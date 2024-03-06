import os
import re
import glob
import importlib.util
import inspect
import sys
import types
import functools
import json
import datetime
import webbrowser
import hashlib
import asyncio
import time

from playwright.sync_api import sync_playwright
from marko.ext.gfm import gfm as markdown
import jinja2
import pytz
import tzlocal
import uuid

from watchtower_browser_testing.tracking_validation import EventQueue, RequestValidator, Validator
from watchtower_browser_testing import exceptions
from watchtower_browser_testing import config
from watchtower_browser_testing import helpers
from watchtower_browser_testing.utils import to_pretty_json


class TestContext(object):

    def __init__(self):

        self.scenario_context = {}
        self.context = {}

    def get(self, key):

        return self.scenario_context.get(key) or self.context.get(key)

    def set(self, key, value, level='test'):

        assert level in ('test', 'scenario'), '`level` should be test or scenario'

        if level == 'test':
            self.context[key] = value
            self.scenario_context.pop(key, None)
        else:
            self.scenario_context[key] = value
            self.context.pop(key, None)

    def reset_scenario_context(self):

        self.scenario_context = {}

    def reset_context(self):

        self.context = {}


class TestResult(object):

    def __init__(self,
                 test_name,
                 browser,
                 measurement_plan=None,
                 scenario=None,
                 event=None,
                 requests=None,
                 starttime=None,
                 endtime=None,
                 ok=True,
                 errors=None,
                 data=None):

        self.test_name = test_name
        self.measurement_plan = measurement_plan
        self.scenario = scenario
        self.event = event
        self.browser = browser
        self.starttime = starttime
        self.endtime = endtime
        self.ok = ok
        self.errors = errors
        self.data = data
        self.requests = requests

    @property
    def css_id(self):

        return 'e_' + '_'.join([str(x) for x in [
            self.measurement_plan,
            self.test_name,
            self.scenario,
            self.event
        ]])

    @property
    def test_id(self):
        
        return hashlib.md5(''.join([str(x) for x in [
            self.measurement_plan,
            self.test_name,
            self.scenario,
            self.event
        ]]).encode('utf-8')).hexdigest()
    
    @staticmethod
    def cast_timezone(t, timezone=None):

        if timezone is None:
            timezone = tzlocal.get_localzone()
        elif isinstance(timezone, str):
            timezone = pytz.timezone(timezone)

        return t.astimezone(timezone)

    def as_dict(self):

        return {
            'measurement_plan': self.measurement_plan,
            'name': self.test_name,
            'scenario': self.scenario,
            'event': self.event,
            'browser': self.browser,
            'ok': self.ok,
            'errors': self.errors,
            'data': self.data,
            'id': self.test_id,
            'starttime': self.starttime,
            'endtime': self.endtime
        }

    def test_report_data(self, timezone=None, json_types=False):
        
        starttime = self.cast_timezone(self.starttime, timezone=timezone)
        endtime = self.cast_timezone(self.endtime, timezone=timezone)

        return {
            'ok': self.ok,
            'browser': self.browser,
            'errors': self.errors,
            'data': self.data,
            'id': self.test_id,
            'starttime': starttime.isoformat() if json_types else starttime,
            'endtime': endtime.isoformat() if json_types else endtime,
            'css_id': self.css_id,
            'requests': self.requests
        }

def new_page_from_gtm(self, ta_page, *args, **kwargs):

    with ta_page.expect_popup() as page_info:
        ta_page.get_by_role("button", name="Reopen").click()
    return page_info.value


class TrackingTest(object):

    browsers = config.DEFAULT_BROWSERS
    storage_attributes = config.DEFAULT_STORAGE_ATTRIBUTES
    async_task_qualnames = ('Request.all_headers',)
    pipeline_patterns = [config.DEFAULT_PIPELINE_PATTERN]

    def __init__(self):

        self.storage = helpers.Storage()
        for storage_attribute in self.storage_attributes:
            if hasattr(self, storage_attribute):
                self.storage[storage_attribute] = getattr(self, storage_attribute)


    def setUpInstance(self,
                      playwright,
                      browser,
                      gtm_web_preview_link=None,
                      tag_assistant_path=None,
                      headless=False,
                      logger=None):

        if logger:
            logger.debug('Setting up instance')

        self.app = getattr(playwright, browser)

        if gtm_web_preview_link and re.match(config.GTM_WEB_PREVIEW_LINK_REGEX, gtm_web_preview_link):
            self.browser = None
            tag_assistant_path = tag_assistant_path or config.DEFAULT_PATH_TO_TAG_ASSISTANT_EXTENSION
            args = [
                f'--disable-extensions-except={tag_assistant_path}',
                f'--load-extension={tag_assistant_path}']
            if headless:
                args.append('--headless=new')
            self.context = self.app.launch_persistent_context(
                '',
                headless=False,
                args=args
            )
            self.ta_page = self.context.new_page()
            self.ta_page.goto(gtm_web_preview_link)
            with self.ta_page.expect_popup() as page_info:
                self.ta_page.get_by_role("button", name="Connect").click()
            self.page = page_info.value
            self.ta_page.get_by_role("button", name="Continue", exact=True).click()
            self.page.close()
            func = functools.partial(new_page_from_gtm, ta_page=self.ta_page)
            self.context.new_page = types.MethodType(func, self.context)

        else:
            
            if logger:
                logger.debug('Launching app')

            self.browser = self.app.launch(headless=headless)

            if logger:
                logger.debug('Creating context')

            self.context = self.browser.new_context()

        self.data_context = TestContext()

    def tearDownInstance(self):

        self.context.close()
        if self.browser:
            self.browser.close()

    def beforeEach(self):

        self.page = self.context.new_page()
        # self.page.set_extra_http_headers(config.IDENTIFY_HEADERS)
        self.data_context.reset_scenario_context()

    def afterEach(self):
        
        self.page.remove_listener('request', self.event_queue.register)
        s = time.time()
        while not all([task.done() for task in asyncio.all_tasks() if task.get_coro().__qualname__ in self.async_task_qualnames]) \
                                                                                                        and time.time() - s < 5.0:
            self.page.wait_for_timeout(100)

        self.page.close()

    def record_events(self):

        self.event_queue = EventQueue(url_patterns=self.pipeline_patterns)
        self.page.on('request', self.event_queue.register)

    def run(self,
            browser=None,
            headless=False,
            gtm_web_preview_link=None,
            tag_assistant_path=None,
            measurement_plan=None,
            report_data=None,
            origin=None,
            logger=None):

        if browser is None:
            browsers = self.browsers
        else:
            browsers = [browser]

        if not origin is None:
            self.storage['origin'] = origin
            self.origin = origin

        self.results = {}
        report_data = report_data or {}

        for browser in browsers:
            
            if logger:
                logger.debug(f'Starting Playwright for {browser}')

            with sync_playwright() as playwright:
                
                

                self.setUpInstance(playwright,
                                   browser,
                                   gtm_web_preview_link=gtm_web_preview_link,
                                   tag_assistant_path=tag_assistant_path,
                                   headless=headless,
                                   logger=logger)

                tests = [func for func in dir(self) if func.startswith(config.SCENARIO_METHOD_PREFIX)]

                for test in tests:

                    scenario = test[len(config.SCENARIO_METHOD_PREFIX):]

                    if logger:
                        logger.debug(f'Running scenario {scenario}')

                    starttime = pytz.utc.localize(datetime.datetime.utcnow())
                    self.beforeEach()

                    try:

                        getattr(self, test)()
                        scenario_success = True
                        scenario_exception = None

                    except Exception as e:
                        
                        scenario_exception = e
                        scenario_success = False

                    self.afterEach()
                    
                    endtime = pytz.utc.localize(datetime.datetime.utcnow())

                    validation_methods = sorted([method for method in dir(self) if method.startswith(config.VALIDATION_METHOD_PREFIX + scenario)])

                    scenario_results = self.results.get(scenario, {})

                    for validation_method in validation_methods:
                        
                        validation_name = validation_method[len(config.VALIDATION_METHOD_PREFIX):]

                        if logger:
                            logger.debug(f'Doing validation {validation_method}')

                        validation_func = getattr(self, validation_method)
                        sig = inspect.signature(validation_func)
                        if len(sig.parameters) > 0:
                            validation_setup = validation_func(storage=self.storage)
                        else:
                            validation_setup = validation_func()

                        validation_result = scenario_results.get(validation_name, {})
                    
                        for event, setup in validation_setup.items():
                            
                            if scenario_success:

                                validator = RequestValidator(**setup)
                                validator.select(self.event_queue.requests)

                                if validator.is_valid():
                                    result = self.result(browser=browser,
                                                measurement_plan=measurement_plan, 
                                                scenario=scenario,
                                                event=event, 
                                                ok=True,
                                                starttime=starttime,
                                                endtime=endtime,
                                                requests={
                                                    'matched': [r.as_dict() for r in validator.matched_requests],
                                                    'unmatched': [r.as_dict() for r in validator.unmatched_requests]
                                                },
                                                data={
                                                    'n_matched_requests': validator.n_matched_requests, 
                                                    **report_data}
                                                )
                                else:
                                    result = self.result(browser=browser, 
                                                measurement_plan=measurement_plan, 
                                                scenario=scenario,
                                                event=event, 
                                                ok=False,
                                                starttime=starttime,
                                                endtime=endtime,
                                                requests={
                                                    'matched': [r.as_dict() for r in validator.matched_requests],
                                                    'unmatched': [r.as_dict() for r in validator.unmatched_requests]
                                                },
                                                errors=validator.errors,
                                                data={'n_matched_requests': validator.n_matched_requests, 
                                                    **report_data}
                                                )
                            
                            else:

                                result = self.result(browser=browser,
                                                     measurement_plan=measurement_plan,
                                                     scenario=scenario,
                                                     event=event,
                                                     ok=False,
                                                     starttime=starttime,
                                                     endtime=endtime,
                                                     requests={'matched': [], 'unmatched': []},
                                                     errors=[{'msg': 'The scenario failed unexpectedly, see the logs for more details', 'exception': str(scenario_exception)}],
                                                     data=report_data)
                                                           
                            validation_result[event] = validation_result.get(event, []) + [result]

                        scenario_results[validation_name] = validation_result

                    self.results[scenario] = scenario_results
                    
                self.tearDownInstance()

    def result(self,
               browser,
               measurement_plan,
               scenario,
               event,
               ok,
               requests,
               starttime=None,
               endtime=None,
               errors=None,
               data=None):

        return TestResult(
            test_name=self.name,
            measurement_plan=measurement_plan,
            scenario=scenario,
            event=event,
            browser=browser,
            ok=ok,
            requests=requests,
            starttime=starttime,
            endtime=endtime,
            errors=errors,
            data=data)

    @property
    def name(self):

        return self.__class__.__name__

    @classmethod
    def scen_methods(cls):

        return [x for x in dir(cls) if x.startswith(config.SCENARIO_METHOD_PREFIX)]

    @classmethod
    def md_description(cls, parent):

        test_name = cls.__name__
        test_id = parent + '_' + cls.__name__

        structure = {'name': test_name,
                     'type': 'test',
                     'id': 't_' + test_id,
                     'description': markdown.convert(helpers.trim(cls.__doc__) or ''),
                     'children': []}

        for scenario_method in cls.scen_methods():

            scenario_name = scenario_method[len(config.SCENARIO_METHOD_PREFIX):]
            scenario_id = test_id + '_' + scenario_name
            scenario_struct = {'name': scenario_name,
                               'type': 'scenario',
                               'id': 's_' + scenario_id,
                               'description': markdown.convert(helpers.trim(getattr(cls, scenario_method).__doc__) or ''),
                               'children': []}
            validation_method_start = config.VALIDATION_METHOD_PREFIX + scenario_method[len(config.SCENARIO_METHOD_PREFIX):]
            validation_methods = sorted([method for method in dir(cls) if method.startswith(validation_method_start)])


            for validation_method in validation_methods:
                
                validation_name = validation_method[len(config.VALIDATION_METHOD_PREFIX):]
                validation_id = scenario_id + '_' + validation_name
                validation_struct = {'name': validation_name,
                                     'type': 'validation',
                                     'id': 'v_' + validation_id,
                                     'description': markdown.convert(helpers.trim(getattr(cls, validation_method).__doc__) or ''),
                                     'children': []}

                val_func = getattr(cls, validation_method)
                sig = inspect.signature(val_func)
                if len(sig.parameters) > 0:
                    val = val_func(storage=helpers.Storage())
                else:
                    val = val_func()


                for event_name, obj in val.items():

                    event_id = scenario_id + '_' + event_name
                    body_validator = obj['validators'].get('body')
                    body_is_dict_list = False
                    if body_validator and isinstance(body_validator, Validator):
                        body_is_dict_list = body_validator.is_dict_list
                        body_validator = body_validator.schema
                    json_string_body = json.dumps(dict(body_validator or {}), indent=4, cls=helpers.ExtendedEncoder)

                    query_validator = obj['validators'].get('query_string')
                    if query_validator and isinstance(query_validator, Validator):
                        query_validator = query_validator.schema
                    json_string_query = json.dumps(dict(query_validator or {}), indent=4, cls=helpers.ExtendedEncoder)

                    check_user_id = not 'check_user_id' in obj['validators'] or obj['validators']['check_user_id']
                    allow_multiple = obj.get('allow_multiple', False)
                    n_matches = obj.get('n_matches')
                    n_matches_lt = obj.get('n_matches_lt')
                    n_matches_gt = obj.get('n_matches_gt')

                    mdstring = cls.create_validation_string(event_name=event_name,
                                                            allow_multiple=allow_multiple,
                                                            check_user_id=check_user_id,
                                                            json_string_query=json_string_query,
                                                            json_string_body=json_string_body,
                                                            body_is_dict_list=body_is_dict_list,
                                                            n_matches=n_matches,
                                                            n_matches_lt=n_matches_lt,
                                                            n_matches_gt=n_matches_gt)

                    event_struct = {'name': event_name,
                                    'id': 'e_' + event_id,
                                    'type': 'event',
                                    'description': markdown.convert(mdstring)}

                    validation_struct['children'].append(event_struct)

                scenario_struct['children'].append(validation_struct)

            structure['children'].append(scenario_struct)

        return structure

    @staticmethod
    def create_validation_string(event_name,
                                 allow_multiple,
                                 check_user_id,
                                 json_string_query,
                                 json_string_body,
                                 body_is_dict_list,
                                 n_matches,
                                 n_matches_lt,
                                 n_matches_gt):

        if not n_matches is None:
            n_requests_string = f'n_matches: {n_matches}'
        elif (not n_matches_gt is None) and (not n_matches_lt is None):
            n_requests_string = f'n_matches in range: [{n_matches_gt}, {n_matches_lt}]'
        elif not n_matches_gt is None:
            n_requests_string = f'n_matches greater than: {n_matches_gt}'
        elif not n_matches_lt is None:
            n_requests_string = f'n_matches less than: {n_matches_lt}'
        else:
            n_requests_string = f'allow_multiple: {"yes" if allow_multiple else "no"}'

        return f'''
<details>
<summary>{event_name} validation (click to see details)</summary>

```
{n_requests_string}

check_user_id: {"yes" if check_user_id else "no"}

query_params_validator: {json_string_query}

body_validator{" (list of objects)" if body_is_dict_list else ""}: {json_string_body}
```
</details>'''

class MeasurementPlan(object):

    test_modules = None
    test_directory = None
    display_name = None
    slug = None

    def __init__(self,
                 test_modules=None,
                 test_directory=None):

        self.test_modules = self.test_modules or test_modules
        self.test_directory = self.test_directory or test_directory
        self.test_results = None
    
    def get_test_modules(self, directory):

        mods = glob.glob(os.path.join(directory, '*.py'))
        test_modules = [os.path.basename(f)[:-3] for f in mods
                        if os.path.isfile(f) and os.path.basename(f).startswith(config.TEST_FILE_PREFIX)]

        if self.test_modules:

            missing = set(self.test_modules) - set(test_modules)
            if len(missing) > 0:
                raise exceptions.NotFoundError(f'Did not find test module(s): {", ".join(missing)}')

            test_modules = [tf for tf in test_modules if tf in self.test_modules]

        return test_modules

    def get_tests(self):

        directory = self.test_directory or os.getcwd()
        test_modules = self.get_test_modules(directory)

        tests = []

        for module_name in test_modules:

            spec = importlib.util.spec_from_file_location(module_name, os.path.join(directory, module_name + '.py'))
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            for attr in module.__dir__():
                if inspect.isclass(getattr(module, attr)) and issubclass(getattr(module, attr), TrackingTest):
                    if any(x.startswith(config.SCENARIO_METHOD_PREFIX) for x in dir(getattr(module, attr))):
                        tests.append({'module': module_name, 'class': getattr(module, attr)})

        missing_validation_methods = []
        for test in tests:
            for method in dir(test['class']):
                if method.startswith(config.SCENARIO_METHOD_PREFIX):
                    scenario = method[len(config.SCENARIO_METHOD_PREFIX):]
                    val_methods = [method for method in dir(test['class']) if method.startswith(config.VALIDATION_METHOD_PREFIX + scenario)]
                    if len(val_methods) == 0:
                        missing_validation_methods.append(
                            test['module'] +
                            '.' + test['class'].__name__ +
                            '.' + config.VALIDATION_METHOD_PREFIX + scenario)

        if len(missing_validation_methods) > 0:
            raise exceptions.NotFoundError(
                f'The following validation methods are missing: {", ".join(missing_validation_methods)}')

        return tests

    def run_tests(self,
                  headless=False,
                  browser=None,
                  gtm_web_preview_link=None,
                  tag_assistant_path=None,
                  origin=None,
                  job_id=None,
                  logger=None):

        self.job_id = job_id or str(uuid.uuid4())

        if not gtm_web_preview_link is None and not re.match(config.GTM_WEB_PREVIEW_LINK_REGEX, gtm_web_preview_link):
            raise exceptions.InvalidInputError(f'This does not look like a valid gtm-preview link: {gtm_web_preview_link}')

        if not gtm_web_preview_link is None and browser != 'chromium':
            raise exceptions.InvalidInputError(f'Debugging with GTM preview only works in chromium, not {browser}')

        if not gtm_web_preview_link is None:
            tag_assistant_path = tag_assistant_path or config.DEFAULT_PATH_TO_TAG_ASSISTANT_EXTENSION
            if not (os.path.isdir(tag_assistant_path)
                    and os.path.isfile(os.path.join(tag_assistant_path, 'manifest.json'))):
                raise exceptions.InvalidInputError(f'No tag assistant extension found at {tag_assistant_path}')

        if logger:
            logger.debug('Getting tests...')

        tests = self.get_tests()

        results = {}
        self.tests_starttime = pytz.utc.localize(datetime.datetime.utcnow())
        for test in tests:

            if logger:
                logger.debug(f'Running {test["class"]} in {test["module"]}')

            test_instance = test['class']()
            report_data = {'module': test['module']}
            test_instance.run(headless=headless,
                              browser=browser,
                              gtm_web_preview_link=gtm_web_preview_link,
                              tag_assistant_path=tag_assistant_path,
                              measurement_plan=self.__class__.__name__,
                              report_data=report_data,
                              origin=origin,
                              logger=logger)
            results[test_instance.name] = test_instance.results

        self.tests_endtime = pytz.utc.localize(datetime.datetime.utcnow())
        self.test_results = results

    def test_report_json(self,
                         timezone=None):
        
        return self.test_report_data(timezone=timezone, json_types=True)

    def test_report_data(self,
                         timezone=None,
                         json_types=False):

        if self.test_results is None:
            raise exceptions.TestError('Run tests firsts')

        if timezone is None:
            timezone = tzlocal.get_localzone()
        elif isinstance(timezone, str):
            timezone = pytz.timezone(timezone)

        time = pytz.utc.localize(datetime.datetime.utcnow()).astimezone(timezone)

        tests_results = {}
        n_errors = 0
        for test_name, test_r in self.test_results.items():
            test_data = {}
            for scenario_name, scenario_results in test_r.items():
                scenario_data = {}
                for val_group_name, val_group in scenario_results.items():
                    val_group_data = {}
                    for event_name, event_results in val_group.items():
                        n_errors += len([r for r in event_results if not r.ok])
                        val_group_data[event_name] = [r.test_report_data(json_types=json_types) for r in event_results]
                    scenario_data[val_group_name] = val_group_data
                test_data[scenario_name] = scenario_data
            tests_results[test_name] = test_data

        return {
            'time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'starttime': self.tests_starttime.astimezone(timezone).isoformat() if json_types else self.tests_starttime.astimezone(timezone),
            'endtime': self.tests_endtime.astimezone(timezone).isoformat() if json_types else self.tests_endtime.astimezone(timezone),
            'n_errors': n_errors,
            'job_id': self.job_id,
            'results': tests_results
        }

    def md_description(self):

        tests = self.get_tests()

        name = self.__class__.__name__
        structure = {'name': name,
                     'id': 'm_' + name,
                     'type': 'measurement_plan',
                     'description': markdown.convert(helpers.trim(self.__doc__) or ''),
                     'children': []}

        for test in tests:
            structure['children'].append(test['class'].md_description(parent=name))


        return structure

    def html_report(self,
                    title='Measurement Plan',
                    test_results=None):

        content = self.md_description()

        test_results = test_results or {}

        return self.render_html(title=title,
                                content=content,
                                test_results=test_results)

    def view_in_browser(self,
                        title='Measurement plan',
                        test_results=None,
                        temp_file_path='temp.html'):

        if not os.path.isabs(temp_file_path):
            temp_file_path = os.path.abspath(os.path.join(os.getcwd(), temp_file_path))

        html = self.html_report(title=title, test_results=test_results)
        with open(temp_file_path, 'w') as f:
            f.write(html)

        webbrowser.open('file://' + os.path.realpath(temp_file_path))

    def hash(self):

        directory = self.test_directory or os.getcwd()
        test_modules = sorted(self.get_test_modules(directory))
        hashes = []

        for module in test_modules:
            with open(os.path.join(directory, module + '.py'), 'rb') as f:
                hashes.append(hashlib.sha256(f.read()).hexdigest())

        with open(inspect.getfile(self.__class__), 'rb') as f:
            hashes.append(hashlib.sha256(f.read()).hexdigest())

        return hashlib.sha256(''.join(hashes).encode('utf-8')).hexdigest()

    @classmethod
    def render_html(cls,
                    title,
                    content,
                    test_results,
                    run_tests_token=None):

        jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(config.TEMPLATES_PATH))
        jenv.filters['pretty_json'] = to_pretty_json
        template = jenv.get_template('measurement_plan.html')

        return template.render(title=title, 
                               content=content,
                               test_results=test_results, 
                               run_tests_token=run_tests_token)