"""
Module CSEPWebTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import unittest, copy, time, os
import urllib2, ClientForm, re

from CSEPLogging import CSEPLogging
# To import on csep-cert 
if os.uname()[0] == 'Linux':
    from mechanize._beautifulsoup import BeautifulSoup
else:
    # To import on Mac
    from BeautifulSoup import BeautifulSoup


#------------------------------------------------------------------------------- 
# CSEPWebTest
# 
# This class is designed for unit testing of the CSEP results viewer
class CSEPWebTest (unittest.TestCase):

    ### Static data of the class
    
    # Top-level URL for the web server to test
    URL = None
    
    # Username for login account to the web server
    Username = None
    
    # Password for login account to the web server    
    Password = None
    
    # Suffix for the forecast group name to exclude from acceptance tests:
    # to avoid testing of forecasts groups with no data at the time of release
    # on csep-op server (while it's available on csep-cert server)
    ExcludeGroupSuffix = None

    # Geographical regions under test in SCEC testing center    
    __CaliforniaRegion = 'california'
    __GlobalRegion = 'global'
    __NWPacificRegion = 'nwpacific'
    __SWPacificRegion = 'swpacific'


    class ForecastGroupInfo (object):
        
        #=======================================================================
        # Initialize ForecastGroupInfo object.
        # 
        # Inputs:
        #         group_models - Set of forecasts models within the group
        #         group_tests - Evaluation tests for the forecast group
        #=======================================================================
        def __init__ (self,
                      group_models,
                      group_tests):
            
            self.models = group_models
            self.tests = group_tests
            
    NTest = 'N'
    LTest = 'L'
    CLTest = 'CL'    
    RTest = 'R'
    STest = 'S'
    MTest = 'M'
    ROCTest = 'ROC'
    MASSTest = 'MASS'
    
    
    # Dictionary of geographical regions and corresponding forecasts groups
    # under test in SCEC testing center
    
    # California's 'one-day-models-optimized' - does not produce results,
    # don't include into final display
    __allRegions = {__CaliforniaRegion : {'one-day-models' : ForecastGroupInfo(set(['ETAS', 'STEP']),
                                                                               set([NTest, LTest, CLTest, MTest, STest, RTest])),
                                          'one-day-models-V9.1' : ForecastGroupInfo(set(['STEP',
                                                                                         'ETAS',
                                                                                         'KJSSOneDayCalifornia']),
                                                                                    set([NTest, LTest, CLTest, MTest, STest, RTest])),
                                          'one-day-models-V10.10' : ForecastGroupInfo(set(['STEP',
                                                                                           'ETAS',
                                                                                           'KJSSOneDayCalifornia',
                                                                                           'STEPJAVA']),
                                                                                    set([NTest, LTest, CLTest, MTest, STest, RTest])),
                                          'one-day-alarm-models-V9.10' : ForecastGroupInfo(set(['GonzalezNearest_OneDayCalifornia_AlarmBased',
                                                                                                'GonzalezUniform_OneDayCalifornia_AlarmBased']),
                                                                                           set([ROCTest, MASSTest])),
                                          'one-day-alarm-models-V10.10' : ForecastGroupInfo(set(['GonzalezNearest_OneDayCalifornia_AlarmBased',
                                                                                                 'GonzalezUniform_OneDayCalifornia_AlarmBased',
                                                                                                 'GonzalezLatestNearest_OneDayCalifornia_AlarmBased']),
                                                                                           set([ROCTest, MASSTest])),
                                                                                           
                                          'three-months-models' : ForecastGroupInfo(set(['EEPAS-0F',
                                                                                         'EEPAS-1F',
                                                                                         'EEPAS-0R',
                                                                                         'EEPAS-1R',
                                                                                         'EEPAS-0S_Combined',
                                                                                         'PPE',
                                                                                         'PPE-S_Combined']),
                                                                                    set([NTest, LTest, CLTest, MTest, STest, RTest])),
                                           # Corrected EEPAS executable by David Rhoades for V9.4 
                                          'three-months-models-V9.4' : ForecastGroupInfo(set(['EEPAS-0F',
                                                                                         'EEPAS-1F',
                                                                                         'EEPAS-0R',
                                                                                         'EEPAS-1R',
                                                                                         'EEPAS-0S_Combined',
                                                                                         'PPE',
                                                                                         'PPE-S_Combined',]),
                                                                                    set([NTest, LTest, CLTest, MTest, STest, RTest])),
                                          'three-months-alarm-models-V9.7' : ForecastGroupInfo(set(['EASTThreeMonthCalifornia_AlarmBased']),
                                                                                    set([ROCTest])),
                                          'three-months-alarm-models-V9.10' : ForecastGroupInfo(set(['EASTThreeMonthCalifornia_AlarmBased',
                                                                                                     'GonzalezUniform_ThreeMonthCalifornia_AlarmBased']),
                                                                                    set([ROCTest, MASSTest])),
                                          'five-year-rate-models' : ForecastGroupInfo(set(['Triple_S_FiveYearCalifornia_RateBased']),
                                                                                      set([NTest, LTest, CLTest, MTest, STest, ROCTest])),
                                          'five-year-alarm-models' : ForecastGroupInfo(set(['Triple_S_FiveYearCalifornia_AlarmBased']),
                                                                                      set([ROCTest])),
                                          'five-year-rate-models-V9.1' : ForecastGroupInfo(set(['Triple_S_FiveYearCalifornia_RateBased',
                                                                                                'KJSSFiveYearCalifornia']),
                                                                                           set([NTest, LTest, CLTest, MTest, STest, RTest, ROCTest, MASSTest])),
                                          'five-year-alarm-models-V9.10' : ForecastGroupInfo(set(['Triple_S_FiveYearCalifornia_AlarmBased',
                                                                                                  'GonzalezUniform_FiveYearCalifornia_AlarmBased']),
                                                                                           set([ROCTest, MASSTest])),
                                          'RELM-mainshock-models' : ForecastGroupInfo(set(['ebel.mainshock',
                                                                                           'kagan_et_al.mainshock',
                                                                                           'ward.geodetic81',
                                                                                           'ward.seismic81',
                                                                                           'helmstetter_et_al.hkj',
                                                                                           'shen_et_al.geodetic.mainshock',
                                                                                           'ward.geodetic85',
                                                                                           'ward.simulation',
                                                                                           'holliday.pi',
                                                                                           'ward.combo81',
                                                                                           'ward.geologic81',
                                                                                           'wiemer_schorlemmer.alm']),
                                                                                      set([NTest, LTest, CLTest, MTest, STest, RTest, ROCTest, MASSTest])),
                                          'RELM-mainshock-models-corrected' : ForecastGroupInfo(set(['ebel.mainshock.corrected',
                                                                                                     'kagan_et_al.mainshock',
                                                                                                     'ward.geodetic85',
                                                                                                     'wiemer_schorlemmer.alm',
                                                                                                     'ebel.mainshock',
                                                                                                     'shen_et_al.geodetic.mainshock',
                                                                                                     'ward.geologic81',
                                                                                                     'helmstetter_et_al.hkj',
                                                                                                     'ward.combo81',
                                                                                                     'ward.seismic81',
                                                                                                     'holliday.pi',
                                                                                                     'ward.geodetic81',
                                                                                                     'ward.simulation']),
                                                                                                 set([NTest, LTest, CLTest, MTest, STest, RTest, ROCTest, MASSTest])),
                                          'RELM-mainshock-aftershock-models' : ForecastGroupInfo(set(['bird_liu.neokinema',
                                                                                                      'helmstetter_et_al.hkj.aftershock',
                                                                                                      'shen_et_al.geodetic.aftershock',
                                                                                                      'ebel.aftershock',
                                                                                                      'kagan_et_al.aftershock']),
                                                                                                 set([NTest, LTest, CLTest, MTest, STest, RTest, ROCTest, MASSTest])),
                                          'RELM-mainshock-aftershock-models-corrected' : ForecastGroupInfo(set(['bird_liu.neokinema',
                                                                                                                'ebel.aftershock',
                                                                                                                'kagan_et_al.aftershock',
                                                                                                                'ebel.aftershock.corrected',
                                                                                                                'helmstetter_et_al.hkj.aftershock',
                                                                                                                'shen_et_al.geodetic.aftershock']),
                                                                                                           set([NTest, LTest, CLTest, MTest, STest, RTest, ROCTest, MASSTest]))},
                                                                                                      
                    __GlobalRegion : {'one-year-alarm-models' : ForecastGroupInfo(set(['Triple_SOneYearGlobal_AlarmBased']),
                                                                                  set([ROCTest])),
                                      'one-year-models' : ForecastGroupInfo(set(['DBMNOneYearGlobal',
                                                                                 'Triple_SOneYearGlobal_RateBased']),
                                                                            set([NTest, LTest, CLTest, STest, RTest, ROCTest, MASSTest])),
                                      'one-year-models-V10.1' : ForecastGroupInfo(set(['DBMNOneYearGlobal',
                                                                                      'Triple_SOneYearGlobal_RateBased',
                                                                                      'KJSSGlobalOneYear']),
                                                                                 set([NTest, LTest, CLTest, STest, RTest, ROCTest, MASSTest])),
                                      'one-day-models-V9.7' : ForecastGroupInfo(set(['KJSSGlobalOneDay']),
                                                                                 set([NTest, LTest, STest])),
                                      'one-day-alarm-models-V10.1' : ForecastGroupInfo(set(['GonzalezNearestV1.01GlobalOneDay_AlarmBased',
                                                                                            'GonzalezUniformV1.01GlobalOneDay_AlarmBased']),
                                                                                       set([ROCTest, MASSTest])),
                                      'one-day-alarm-models-V10.10' : ForecastGroupInfo(set(['GonzalezNearestV1.01GlobalOneDay_AlarmBased',
                                                                                             'GonzalezUniformV1.01GlobalOneDay_AlarmBased',
                                                                                             'GonzalezLatestNearestGlobalOneDay_AlarmBased']),
                                                                                        set([ROCTest, MASSTest]))},
                                          
                    __NWPacificRegion : {'one-day-models' : ForecastGroupInfo(set(['KJSSOneDayNWPacific']),
                                                                              set([NTest, LTest, CLTest, STest])),
                                         'one-year-alarm-models' : ForecastGroupInfo(set(['Triple_SNWPacific_AlarmBased']),
                                                                                     set([ROCTest])),
                                         'one-year-models' : ForecastGroupInfo(set(['KJSSOneYearNWPacific',
                                                                                    'Triple_SNWPacific']),
                                                                               set([NTest, LTest, CLTest, STest, RTest, ROCTest, MASSTest])),
                                         'one-year-models-V9.1' : ForecastGroupInfo(set(['KJSSOneYearNWPacific',
                                                                                         'DBMOneYearNWPacific',
                                                                                         'Triple_SNWPacific']),
                                                                                    set([NTest, LTest, CLTest, STest, RTest, ROCTest, MASSTest])),
                                         'one-day-alarm-models-V10.1' : ForecastGroupInfo(set(['GonzalezNearestV1.01OneDayNWPacific_AlarmBased',
                                                                                               'GonzalezUniformV1.01OneDayNWPacific_AlarmBased']),
                                                                                          set([ROCTest, MASSTest])),
                                         'one-day-alarm-models-V10.10' : ForecastGroupInfo(set(['GonzalezNearestV1.01OneDayNWPacific_AlarmBased',
                                                                                                'GonzalezUniformV1.01OneDayNWPacific_AlarmBased',
                                                                                                'GonzalezLatestNearestWesternPacific_OneDayNWPacific_AlarmBased']),
                                                                                           set([ROCTest, MASSTest]))},
                                             
                    __SWPacificRegion : {'one-day-models' : ForecastGroupInfo(set(['KJSSOneDaySWPacific']),
                                                                              set([NTest, LTest, CLTest, STest])), 
                                         'one-year-alarm-models' : ForecastGroupInfo(set(['Triple_SSWPacific_AlarmBased']),
                                                                                     set([ROCTest])),
                                         'one-year-models' : ForecastGroupInfo(set(['KJSSOneYearSWPacific',
                                                                                    'Triple_SSWPacific']),
                                                                               set([NTest, LTest, CLTest, STest, RTest, ROCTest, MASSTest])),
                                         'one-year-models-V9.1' : ForecastGroupInfo(set(['KJSSOneYearSWPacific',
                                                                                         'DBMOneYearSWPacific',
                                                                                         'Triple_SSWPacific']),
                                                                                    set([NTest, LTest, CLTest, STest, RTest, ROCTest, MASSTest])),
                                         'one-day-alarm-models-V10.1' : ForecastGroupInfo(set(['GonzalezNearestV1.01OneDaySWPacific_AlarmBased',
                                                                                               'GonzalezUniformV1.01OneDaySWPacific_AlarmBased']),
                                                                                          set([ROCTest, MASSTest])),
                                         'one-day-alarm-models-V10.10' : ForecastGroupInfo(set(['GonzalezNearestV1.01OneDaySWPacific_AlarmBased',
                                                                                                'GonzalezUniformV1.01OneDaySWPacific_AlarmBased',
                                                                                                'GonzalezLatestNearestWesternPacific_OneDaySWPacific_AlarmBased']),
                                                                                           set([ROCTest, MASSTest]))}}
    
    # Web form controls
    __regionControl = 'region'
    __modelControl = 'model'
    
    __nameAttribute = 'name'
    __keyAttribute = 'key'

    # Web form option to bypass in tests 
    __chooseFormKeyword = 'Choose a Model'
        
    
    #--------------------------------------------------------------------
    #
    # Set up testing scenario.
    #
    # Input: 
    #        None.
    # 
    def setUp (self):
        
        """Initialize connection to the server and collect all available forms."""

        # create a password manager
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        
        # Add the username and password.
        # If we knew the realm, we could use it instead of ``None``.
        password_mgr.add_password(None, 
                                  CSEPWebTest.URL, 
                                  CSEPWebTest.Username, 
                                  CSEPWebTest.Password)
        
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        
        # create "opener" (OpenerDirector instance)
        opener = urllib2.build_opener(handler)
        
        # Install the opener.
        # Now all calls to urllib2.urlopen use our opener.
        urllib2.install_opener(opener)
        
        
        response = urllib2.urlopen(CSEPWebTest.URL)
        
        # All forms (for all forecasts groups of all testing regions)
        self.__forms = ClientForm.ParseResponse(response, 
                                                backwards_compat=False)

        #print "FIRST FORM", self.__forms[0]
        # Dictionary of regions and corresponding forecasts groups forms
        self.__regions = {}
        # Sort forms by geographical region
        for each_form in self.__forms:
            
            # Extract region control of the form
            region_control = each_form.find_control(CSEPWebTest.__regionControl) 

            # Find forms that represent forecast groups of selected testing region
            self.__regions.setdefault(region_control.value, 
                                      []).append(each_form)
            
        # Examine form in detail
        show_debug = False
        if show_debug is True:
            form = self.__forms[0]
            
            
        #FORM: <RELM-mainshock-aftershock-models-plot POST http://intensity.usc.edu/csep/main.php application/x-www-form-urlencoded
        #  <SelectControl(key=[*7, 8, 9, 10, 11])>
        #  <HiddenControl(model=) (readonly)>
        #  <HiddenControl(region=california) (readonly)>
        #  <SubmitControl(go=go) (readonly)>>
            
            region_control = form.find_control('region')
        
            print "REGION attribs", region_control.name, region_control.value, region_control.type
            print "REGION (control)", region_control
            print "REGION (disabled)", region_control.disabled
            print "REGION (readonly)", region_control.readonly
            print "REGION labels", region_control.get_labels
            
            go_control = form.find_control('go')
            print "GO control:", go_control, "disabled", go_control.disabled, \
                  "name=", go_control.name, \
                  "value=", go_control.value, \
                  "type=", go_control.type
            
        #    for item in go_control.items:
        #        print "all go:", item.name, item.id, item.attrs 
                
        
            model_control = form.find_control('model', type='hidden')
            print 'MODEL labels', model_control.get_labels()
            print "MODEL:", model_control
            
            region_key_control = form.find_control('key', type='select')
            print "KEY (disabled)", region_key_control.disabled
            print "KEY (readonly)", region_key_control.readonly
            
            #<div id="california-RELM-mainshock-aftershock-models" class="menu_model">
            #<form name="RELM-mainshock-aftershock-models-plot" method="post" action="main.php" target="main">
            #<select name="key"><option value="7">bird_liu.neokinema</option>
            #<option value="8">ebel.aftershock</option>
            #<option value="9">helmstetter_et_al.hkj.aftershock</option>
            #<option value="10">kagan_et_al.aftershock</option>
            #<option value="11">shen_et_al.geodetic.aftershock</option></select>
            print "KEY", region_key_control, \
                  "name=", region_key_control.name, \
                  "value=", region_key_control.value, \
                  "type=", region_key_control.type
            
            for item in form.find_control("key").items:
                print "all keys:", item.name, item.id, item.attrs

#REGION (control) <HiddenControl(region=california) (readonly)>
#REGION (disabled) False
#REGION (readonly) True
#REGION labels <bound method HiddenControl.get_labels of <ClientForm.HiddenControl instance at 0x157c5f8>>
#GO control: <SubmitControl(go=go) (readonly)> disabled False name= go value= go type= submit
#MODEL labels []
#MODEL: <HiddenControl(model=) (readonly)>
#KEY (disabled) False
#KEY (readonly) False
#KEY <SelectControl(key=[*6, 7, 8, 9, 10])> name= key value= ['6'] type= select
#all keys: 6 None {'contents': 'bird_liu.neokinema', 'value': '6', 'label': 'bird_liu.neokinema'}
#all keys: 7 None {'contents': 'ebel.aftershock', 'value': '7', 'label': 'ebel.aftershock'}
#all keys: 8 None {'contents': 'helmstetter_et_al.hkj.aftershock', 'value': '8', 'label': 'helmstetter_et_al.hkj.aftershock'}
#all keys: 9 None {'contents': 'kagan_et_al.aftershock', 'value': '9', 'label': 'kagan_et_al.aftershock'}
#all keys: 10 None {'contents': 'shen_et_al.geodetic.aftershock', 'value': '10', 'label': 'shen_et_al.geodetic.aftershock'}
        
            
            form.set_all_readonly(False)
        
            ### Reset controls
            form['region'] = 'california'
            form['key'] = ["8"]
            
            
            #form.click() returns a urllib2.Request object
            # (see HTMLForm.click.__doc__ if you don't have urllib2)
            print "AFTER CLICK:", urllib2.urlopen(form.click()).read()
            
            #print "FORM after click()", form   
        
        
    #===========================================================================
    # Test if expected regions are displayed by the web viewer. 
    #===========================================================================
    def testAllRegionsExistence (self):
        """ Test that all geographical regions exist for the display."""
   
        # Regions as reported by the web site
        web_regions = set(self.__regions.keys())

        reference_regions = set(CSEPWebTest.__allRegions.keys())
        
        # Fail if regions don't match
        self.failIf(len(web_regions.difference(reference_regions)) != 0,
                    "Expected geographical regions %s, got %s" %(reference_regions,
                                                                 web_regions))


    #===========================================================================
    # Test existence of forecasts groups for California testing region within 
    # SCEC testing center.
    #===========================================================================
    def testCaliforniaForecastsGroupsExistence (self):
        """ Test that all geographical regions display expected set of forecasts \
groups (specific to the region)."""
   
        self.__regionsGroupsExistence(CSEPWebTest.__CaliforniaRegion)


    #===========================================================================
    # Test existence of forecasts groups for Global testing region within 
    # SCEC testing center.
    #===========================================================================
    def testGlobalForecastsGroupsExistence (self):
        """ Test that all geographical regions display expected set of forecasts \
groups (specific to the region)."""
   
        self.__regionsGroupsExistence(CSEPWebTest.__GlobalRegion)


    #===========================================================================
    # Test existence of forecasts groups for NWestern Pacific testing region within 
    # SCEC testing center.
    #===========================================================================
    def testNWPacificForecastsGroupsExistence (self):
        """ Test that all geographical regions display expected set of forecasts \
groups (specific to the region)."""
   
        self.__regionsGroupsExistence(CSEPWebTest.__NWPacificRegion)


    #===========================================================================
    # Test existence of forecasts groups for SWestern Pacific testing region within 
    # SCEC testing center.
    #===========================================================================
    def testSWPacificForecastsGroupsExistence (self):
        """ Test that all geographical regions display expected set of forecasts \
groups (specific to the region)."""
   
        self.__regionsGroupsExistence(CSEPWebTest.__SWPacificRegion)
        

    #===========================================================================
    # Test presence of all forecasts models within each group of California 
    # testing region.
    #===========================================================================
    def testCaliforniaModelsExistence (self):
        """ Test that California region contains expected forecasts models within \
each group."""
   
        self.__groupModelsExistence(CSEPWebTest.__CaliforniaRegion)


    #===========================================================================
    # Test presence of all forecasts models within each group of Global 
    # testing region.
    #===========================================================================
    def testGlobalModelsExistence (self):
        """ Test that Global region contains expected forecasts models within \
each group."""
   
        self.__groupModelsExistence(CSEPWebTest.__GlobalRegion)


    #===========================================================================
    # Test presence of all forecasts models within each group of NW Pacific 
    # testing region.
    #===========================================================================
    def testNWPacificModelsExistence (self):
        """ Test that NW Pacific region contains expected forecasts models within \
each group."""
   
        self.__groupModelsExistence(CSEPWebTest.__NWPacificRegion)


    #===========================================================================
    # Test presence of all forecasts models within each group of SW Pacific 
    # testing region.
    #===========================================================================
    def testSWPacificModelsExistence (self):
        """ Test that SW Pacific region contains expected forecasts models within \
each group."""
   
        self.__groupModelsExistence(CSEPWebTest.__SWPacificRegion)


    #===========================================================================
    # Test presence of all expected evaluation tests plots and forecasts models
    # maps within each group of California testing region.
    #===========================================================================
    def testCaliforniaModelsPlots (self):
        """ Test that California forecasts models within each group display \
expected evaluation tests, forecast maps, and plots for the tests."""
   
        self.__modelMapAndTests(CSEPWebTest.__CaliforniaRegion)


    #===========================================================================
    # Test presence of all expected evaluation tests plots and forecasts models
    # maps within each group of California testing region.
    #===========================================================================
    def testGlobalModelsPlots (self):
        """ Test that Global forecasts models within each group display \
expected evaluation tests, forecast maps, and plots for the tests."""
   
        self.__modelMapAndTests(CSEPWebTest.__GlobalRegion)


    #===========================================================================
    # Test presence of all expected evaluation tests plots and forecasts models
    # maps within each group of NW Pacific testing region.
    #===========================================================================
    def testNWPacificModelsPlots (self):
        """ Test that NW Pacific forecasts models within each group display \
expected evaluation tests, forecast maps, and plots for the tests."""
   
        self.__modelMapAndTests(CSEPWebTest.__NWPacificRegion)


    #===========================================================================
    # Test presence of all expected evaluation tests plots and forecasts models
    # maps within each group of SW Pacific testing region.
    #===========================================================================
    def testSWPacificModelsPlots (self):
        """ Test that NW Pacific forecasts models within each group display \
expected evaluation tests, forecast maps, and plots for the tests."""
   
        self.__modelMapAndTests(CSEPWebTest.__SWPacificRegion)


    #===========================================================================
    # Test presence of all expected plots for each model within each forecast
    # group of specified testing region.
    # Inputs:
    #         region_name - Name of the testing region to check forecasts models
    #                       for.  
    #
    # Output: None.
    #===========================================================================
    def __modelMapAndTests (self, region_name):
        """ Test that each model within each forecast group of the testing \
region displays expected plots."""


        # Iterate through all forecasts groups of the region
        for each_form in self.__regions[region_name]:

            group_name = self.__stripName(each_form.attrs[CSEPWebTest.__nameAttribute])
            
            if CSEPWebTest.ExcludeGroupSuffix is not None and \
               group_name.endswith(CSEPWebTest.ExcludeGroupSuffix) is True:
                CSEPLogging.getLogger(__name__).info('Skipping models images for %s group' %group_name)
                continue
            
            CSEPLogging.getLogger(__name__).info('Testing models images for %s group' %group_name)

            # Set all fields writable, so we can submit the form
            each_form.set_all_readonly(False)
            
            # Accumulate plots errors for the group 
            group_errors = []
            
            # Submit a form by iterating through all possible forecasts models of the group
            for each_model in each_form.find_control(CSEPWebTest.__keyAttribute).items:

                if CSEPWebTest.__chooseFormKeyword in each_model.attrs['label']:
                    continue
                
                # each key element of the form will have the following attributes: 
                # {'contents': 'bird_liu.neokinema', 'value': '6', 'label': 'bird_liu.neokinema'}
                each_form[CSEPWebTest.__keyAttribute] = [each_model.attrs['value']]
                 
                #form.click() returns a urllib2.Request object
                request = urllib2.urlopen(each_form.click())
                html_parser = BeautifulSoup(request.read())
                request.close()
                
                # Allow some time between requests to the web server                     
                time.sleep(1)
        
                display_is_on = False
                if display_is_on is True:
                    CSEPLogging.getLogger(__name__).info( "REQUEST for " + each_model.attrs['label'] + html_parser.prettify()) 

                # Reference set of tests for the model - exclude R-test
                # since web form lists R-test in a separate <select> option
                reference_tests = copy.deepcopy(self.__allRegions[region_name][group_name].tests)
                reference_tests.discard(CSEPWebTest.RTest) 

                #=======================================================
                # Check for available tests (except for R-test)
                #=======================================================
                error = self.__modelEvaluationTests(html_parser,
                                                    each_model, 
                                                    reference_tests)
                if error is not None:
                    group_errors.append(error)


                #=======================================================
                # Check for forecast map
                #=======================================================
                error = self.__modelMap(html_parser, 
                                        each_model)
                if error is not None:
                    group_errors.append(error)
                

                #=======================================================
                # Check for plots of each evaluation test (except for R-test)
                #=======================================================
                error = self.__modelPlots(html_parser, 
                                          each_model,
                                          reference_tests)
                if error is not None:
                    group_errors.append(error)


                #=======================================================
                # Check for plots of each evaluation test (except for R-test)
                #=======================================================
                error = self.__modelRPlots(html_parser, 
                                           each_model,
                                           self.__allRegions[region_name][group_name])
                if error is not None:
                    group_errors.append(error)

            # end of each_model
            
            self.failIf(len(group_errors) != 0,
                        "%s forecast group for %s testing region errors: \n%s" \
                        %(group_name, region_name, '\n'.join(group_errors)))
                        


    #===========================================================================
    # Test presence of model evaluation tests except for the R-test since it has 
    # a separate <select> for it.
    # Inputs:
    #         html_parser - Parser for the model submitted form
    #         each_model - Model object
    #         reference_tests - Expected tests for the model
    #
    # Output: Error message if any
    #
    # An example of form that gets parsed for information:
    #===========================================================================
    #  <select name="plots" onchange="
    #    MM_showHideLayers(mactive,'','hide');
    #    MM_showHideLayers(this.options[this.selectedIndex].value,'','show');
    #    mactive=this.options[this.selectedIndex].value;">
    #   <option value="">
    #    ---Test Results---
    #   </option>
    #   /var/www/html/csep/data/us/usc/california/RELM-mainshock-aftershock-models/results/
    #   <option value="L">
    #    L
    #   </option>
    #   /var/www/html/csep/data/us/usc/california/RELM-mainshock-aftershock-models/results/
    #   <option value="M">
    #    M
    #   </option>
    #   /var/www/html/csep/data/us/usc/california/RELM-mainshock-aftershock-models/results/
    #   <option value="N">
    #    N
    #   </option>
    #   /var/www/html/csep/data/us/usc/california/RELM-mainshock-aftershock-models/results/
    #   <option value="S">
    #    S
    #   </option>
    #   /var/www/html/csep/data/us/usc/california/RELM-mainshock-aftershock-models/results//var/www/html/csep/data/us/usc/california/RELM-mainshock-aftershock-models/results/
    #   <option value="ROC">
    #    ROC
    #   </option>
    #   /var/www/html/csep/data/us/usc/california/RELM-mainshock-aftershock-models/results/
    #   <option value="Molchan">
    #    Molchan
    #   </option>
    #  </select>
    #
    #===========================================================================
    def __modelEvaluationTests (self, 
                                html_parser, 
                                each_model,
                                reference_tests):
        """ Check for available tests for the model."""


        # Extract <select name='plots'> element that contains all
        # available tests for the model in <option> children
        web_tests = set([])
        
#        print "Parser=", html_parser
#        tests_select_element = html_parser.find('select')
#        print "Parser <select>:", tests_select_element

        tests_select_element = html_parser.find('select', 
                                                {'name' : 'plots'})
        for each_test in tests_select_element.fetch('option'):
            web_tests.add(str(each_test['value']))
            
        # Exclude empty strings from the set: first option is empty
        web_tests.discard('')    
        
        diff_of_tests = reference_tests.difference(web_tests)
        if len(diff_of_tests) != 0:
            return "Unexpected difference of evaluation tests set for %s forecast model: %s. Expected %s, got %s." \
                    %(each_model.attrs['label'], 
                      diff_of_tests, 
                      reference_tests, 
                      web_tests)

        # No error occurred
        return None
    

    #===========================================================================
    # Test presence of forecast model map.
    # Inputs:
    #         html_parser - Parser for the model submitted form
    #         each_model - Model object
    #
    # Output: Error message if any
    #
    # An example of form that gets parsed for information:
    #===========================================================================
    #  <div id="bird_liu.neokinema-map" class="maps">
    #   <img src="tmp//scec.csep.RELMTest.Map_bird_liu.neokinema.png.1243962585.554721.1.png" />
    #  </div>
    #
    #===========================================================================
    def __modelMap (self, 
                    html_parser, 
                    each_model):
        """ Check for the presence of model map."""

        maps = []
        map_select_element = html_parser.find('div', 
                                              {'class' : 'maps'})
        for each_map in map_select_element.fetch('img'):
            maps.append(str(each_map['src']))
        
        # Only one forecast map is expected
        self.failIf(len(maps) != 1,
                    "Forecast map is expected for %s model, found: %s" \
                    %(each_model.attrs['label'], 
                      maps)) 

        # Check that model's map is displayed
        match_model_name = re.search('(?<=.Map_)%s' %each_model.attrs['label'], 
                                     maps[0])
        match_map_extension = re.search('(?<=.png)', maps[0]) 

        if match_model_name is None or \
           match_map_extension is None:
             
           return "Forecast map name %s doesn't match expected pattern '*Map_%s*.png*': %s" \
                    %(maps[0], 
                      each_model.attrs['label'],
                      map_select_element)

        return None
    

    #===========================================================================
    # Test presence of plots for evaluation tests (except for the R-test)
    # Inputs:
    #         html_parser - Parser for the model submitted form
    #         each_model - Model object
    #         reference_tests - Expected tests for the model
    #
    # Output: Error message if any
    #
    # An example of form that gets parsed for information:
    #===========================================================================
    #  <div id="L" class="plots">
    #   <img src="tmp//intermediate.rTest_L-Test_bird_liu.neokinema-fromXML.svg.png" />
    #  </div>
    #  <div id="M" class="plots">
    #   <img src="tmp//intermediate.rTest_M-Test_bird_liu.neokinema-fromXML.svg.png" />
    #  </div>
    #  <div id="N" class="plots">
    #   <img src="tmp//intermediate.rTest_N-Test_bird_liu.neokinema-fromXML.svg.png" />
    #  </div>
    #  <div id="S" class="plots">
    #   <img src="tmp//intermediate.rTest_S-Test_bird_liu.neokinema-fromXML.svg.png" />
    #  </div>
    #  <div id="ROC" class="plots">
    #   <img src="tmp//intermediate.rTest_ROC-Test_bird_liu.neokinema-fromXML.svg.png" />
    #  </div>
    #  <div id="Molchan" class="plots">
    #   <img src="tmp//intermediate.rTest_Molchan-Test_bird_liu.neokinema-fromXML.svg.png" />
    #  </div>
    #
    #===========================================================================
    def __modelPlots (self, 
                      html_parser, 
                      each_model,
                      reference_tests):
        """ Check for the presence of model evaluation tests plots."""
    
        plots_tests = set([])

        for each_plot in html_parser.findAll('div', 
                                             {'class' : 'plots'}):
            # Find Child <img> element
            image = each_plot.find('img')
            
            test_name = str(each_plot['id'])
            plots_tests.add(test_name)
            plot_filename = str(image['src'])
            
            match_model_name = re.search('(?<=%s-Test_)%s(_[0-9]+_[0-9]+_[0-9][0-9][0-9][0-9])?-fromXML' %(test_name,
                                                                                                           each_model.attrs['label']), 
                                         plot_filename)
            
            match_plot_extension = re.search('(?<=.png)', 
                                             plot_filename)
            
            if match_model_name is None or \
               match_plot_extension is None:
                
               return "Plot filename %s doesn't match expected pattern '*%s-Test_%s(_DD_MM_YYYY)-fromXML*.png*'" \
                      %(plot_filename, 
                        test_name, 
                        each_model.attrs['label'])
            
            
        diff_of_plots_tests = reference_tests.difference(plots_tests)
        if len(diff_of_plots_tests) != 0:
            
            return "Unexpected difference for %s model plots: %s. Expected plots for %s tests, got for %s." \
                   %(each_model.attrs['label'], 
                     diff_of_plots_tests, 
                     reference_tests, 
                     plots_tests)
    
        return None
    

    #===========================================================================
    # Test presence of plots for R evaluation tests
    # Inputs:
    #         html_parser - Parser for the model submitted form
    #         each_model - Model object
    #         group_info - Reference ForecastGroupInfo object for the model
    #
    # Output: Error message if any
    #
    # An example of form that gets parsed for information:
    #===========================================================================
    #  <select name="rplots" onchange="
    #    MM_showHideLayers(mactive,'','hide');
    #    MM_showHideLayers(this.options[this.selectedIndex].value,'','show');
    #    mactive=this.options[this.selectedIndex].value;">
    #   <option value="">
    #    ---R-Test Comparisons---
    #   </option>
    #   <option value="ebel.aftershock-bird_liu.neokinema">
    #    ebel.aftershock
    #   </option>
    #   <option value="helmstetter_et_al.hkj.aftershock-bird_liu.neokinema">
    #    helmstetter_et_al.hkj.aftershock
    #   </option>
    #   <option value="kagan_et_al.aftershock-bird_liu.neokinema">
    #    kagan_et_al.aftershock
    #   </option>
    #   <option value="shen_et_al.geodetic.aftershock-bird_liu.neokinema">
    #    shen_et_al.geodetic.aftershock
    #   </option>
    #  </select>
    #  <div id="ebel.aftershock-bird_liu.neokinema" class="rplots">
    #   <img src="tmp/intermediate.rTest_R-Test_bird_liu.neokinema-fromXML_ebel.aftershock-fromXML.svg.png" />
    #  </div>
    #  <div id="helmstetter_et_al.hkj.aftershock-bird_liu.neokinema" class="rplots">
    #   <img src="tmp/intermediate.rTest_R-Test_bird_liu.neokinema-fromXML_helmstetter_et_al.hkj.aftershock-fromXML.svg.png" />
    #  </div>
    #  <div id="kagan_et_al.aftershock-bird_liu.neokinema" class="rplots">
    #   <img src="tmp/intermediate.rTest_R-Test_bird_liu.neokinema-fromXML_kagan_et_al.aftershock-fromXML.svg.png" />
    #  </div>
    #  <div id="shen_et_al.geodetic.aftershock-bird_liu.neokinema" class="rplots">
    #   <img src="tmp/intermediate.rTest_R-Test_bird_liu.neokinema-fromXML_shen_et_al.geodetic.aftershock-fromXML.svg.png" />
    #  </div>
    #
    #===========================================================================
    def __modelRPlots (self, 
                      html_parser, 
                      each_model,
                      group_info):
        """ Check for the presence of model R evaluation tests plots."""

        
        # R-test is not invoked for the group
        if CSEPWebTest.RTest not in group_info.tests:
            return None
        
        
        # Since R-test requires two models, check that there are plots for all
        # possible combinations of the 'each_model' with other models in the 
        # group
        web_other_models = set([])
        
        models_select_element = html_parser.find('select', 
                                                {'name' : 'rplots'})
        for each_option in models_select_element.fetch('option'):
            web_other_models.add(str(each_option.string))
            
        # Exclude empty strings from the set: first option is empty
        web_other_models.discard('---R-Test Comparisons---')    
        
        # Models within group - exclude model itself
        reference_models = copy.deepcopy(group_info.models)
        reference_models.discard(str(each_model.attrs['label']))
        
#        print "MODEL:", each_model.attrs['label'], "REF MODELS", reference_models
        diff_of_models = reference_models.difference(web_other_models)
        if len(diff_of_models) != 0:
            return "Unexpected difference in R-test selection for %s model: %s. Expected %s, got %s." \
                    %(each_model.attrs['label'], 
                      diff_of_models, 
                      reference_models, 
                      web_other_models)
        

        # Make sure filename contains a unique combination of each_model with
        # every other model in the group:
        # if filename matched any of the models in reference_models, remove it
        # from the list: any remaining models will have missing plots
        for each_plot in html_parser.findAll('div', 
                                             {'class' : 'rplots'}):
            # Find child <img> element
            image = each_plot.find('img')
            plot_filename = str(image['src'])
#            print "CHECKING ", plot_filename

            # Match file extension
            match_plot_extension = re.search('(?<=.png)', 
                                             plot_filename)
            # Match selected model
            match_model = re.search('(?<=_)%s-fromXML' %each_model.attrs['label'], plot_filename)
            if match_plot_extension is None or \
               match_model is None:
                
                return "%s plot file is not matching '*_%s*.png*' pattern" \
                       %(plot_filename, each_model.attrs['label']) 
            
#            print "REF MODELS", reference_models
            for each_other_model in reference_models:
#                print "Checking %s for %s model" %(plot_filename,
#                                                   each_other_model)
                match_other_model = re.search('(?<=_)%s-fromXML' %each_other_model, plot_filename)
                
                if match_other_model is not None:
                    # Found the match
#                    print  "MATCHED", each_other_model
                    reference_models.discard(each_other_model)
                    break
                    
        if len(reference_models) != 0:
            return "R-plots are missing for combination of %s model with %s" \
                  %(each_model.attrs['label'], 
                    reference_models)

        return None


    #===========================================================================
    # Test presence of all forecasts models within each group of specified 
    # testing region.
    # Inputs:
    #         region_name - Name of the testing region to check forecasts groups
    #                       for.  
    #
    # Output: None.
    #===========================================================================
    def __groupModelsExistence (self, region_name):
        """ Test that testing region contains expected forecasts models within \
each group."""
   

        # Forecast groups for the region as reported by the web site
        web_groups = {}
        for each_form in self.__regions[region_name]:
            
            web_groups[self.__stripName(each_form.attrs[CSEPWebTest.__nameAttribute])] = each_form 


        #print "REGION FORMS:", web_groups
        
        # Check if expected forecast models are within the group
        for group_name, group_form in web_groups.iteritems():
            
            if CSEPWebTest.ExcludeGroupSuffix is not None and \
               group_name.endswith(CSEPWebTest.ExcludeGroupSuffix) is True:
                CSEPLogging.getLogger(__name__).info('Skipping models for %s group' %group_name)
                continue
            
            web_models = set([])
            # each key element of the form will have the followingattrs: 
            # {'contents': 'bird_liu.neokinema', 'value': '6', 'label': 'bird_liu.neokinema'}
            for each_model in group_form.find_control(CSEPWebTest.__keyAttribute).items:
                web_models.add(CSEPWebTest.__stripDate(each_model.attrs['label']))
            
            reference_models = CSEPWebTest.__allRegions[region_name][group_name].models
            diff_of_models = reference_models.difference(web_models)
            
            if len(diff_of_models) > 0:
                CSEPLogging.getLogger(__name__).error("Unexpected difference for %s %s forecast group: %s. Expected %s, got %s." \
                            %(region_name, 
                              group_name, 
                              diff_of_models, 
                              reference_models, 
                              web_models))
                        
            self.failIf(len(diff_of_models) > 0,
                        "Unexpected difference for %s %s forecast group: %s. Expected %s, got %s." \
                        %(region_name, 
                          group_name, 
                          diff_of_models, 
                          reference_models, 
                          web_models))


    #===========================================================================
    # Strip date in 'MM_DD_YYYY' format from the model name.
    #
    # Inputs:
    #         name - Model name
    # 
    # Output: Name with stripped date    
    #===========================================================================
    @staticmethod
    def __stripDate (name):
        """ Remove date string from forecast filename."""
   

        # Strip forecast start date from the filename: csep-cert will have other
        # start dates than csep-op will for the same forecast model due to the
        # early testing
        return re.sub('_'.join(['',
                                '[0-9]+',
                                '[0-9]+',
                                '[0-9][0-9][0-9][0-9]']), 
                      "", name)


    #===========================================================================
    # Test existence of forecasts groups for specified testing region.
    #
    # Inputs:
    #         region_name - Name of the testing region to check forecasts groups
    #                       for.  
    #
    # Output: None.
    #===========================================================================
    def __regionsGroupsExistence (self, region_name):
        """ Test that expected forecasts groups exist for geographical region."""
   

        web_groups = set([])
        
        for each_form in self.__regions[region_name]:
            
            web_groups.add(each_form.attrs[CSEPWebTest.__nameAttribute])

        # Expected set of 
        reference_groups = set(CSEPWebTest.__allRegions[region_name].keys())
        
        # Strip '-plot' from each group name - appended by web server
        web_groups_stripped_names = self.__stripName(web_groups)
        diff_of_groups = web_groups_stripped_names.difference(reference_groups)

        # Fail if collection of groups for California doesn't match
        self.failIf(len(diff_of_groups) != 0,
                    "Unexpected difference for %s forecasts groups: %s. \
                     Expected %s forecasts groups, got %s" %(region_name,
                                                             diff_of_groups,
                                                             reference_groups,
                                                             web_groups_stripped_names))


    #===========================================================================
    # Strip '-plots' keyword from forecast group name that web server reports.
    #
    # Inputs:
    #         name_list - List of names to strip or a single name
    #         keyword - Keyword to strip from name_list. Default is '-plots'.
    # 
    # Output: Name with removed token, or a list of names with removed tokens    
    #===========================================================================
    def __stripName (self, name_list, keyword='-plot'):
        """ Remove specified token from name or a list of names."""
   
        # A single name string is provided
        if isinstance(name_list, str):
            return name_list.replace(keyword, '')
        else:
            return set([each_name.replace(keyword, '') for each_name in name_list])
        

#--------------------------------------------------------------------------------
#
# CSEPWebTest.
#
# This module is designed as an acceptance test suite for the CSEP results
# web viewer.
#
# Invoke the module to test results published to intensity.usc.edu by csep-cert server: 
# python CSEPWebTest.py --url=http://intensity.usc.edu/csep
# OR to test results published to  us.cseptesting.org by csep-op server:
# python CSEPWebTest.py
#
if __name__ == '__main__':
   
    import optparse
    
    command_options = optparse.OptionParser()
    
    command_options.add_option('--user',
                               dest='username',
                               default='cseptesting',
                               help="User name for an account to access web viewer. \
Default is 'cseptesting'.")

    command_options.add_option('--password',
                               dest='userpass',
                               default='version1.0',
                               help="Password for an account to access web viewer. \
Default is 'version1.0'.")

    command_options.add_option('--url',
                               dest='top_level_url',
                               default='http://scec.usc.edu/csep/webviewer/scec',
                               help="Top-level URL to connect to. \
Default is 'http://scec.usc.edu/csep/webviewer/scec'. Please specify 'http://intensity.usc.edu/csep/cert' for certification server.")


    command_options.add_option('--excludeGroup',
                               dest='exclude_group_suffix',
                               type='str',
                               default=None,
                               help="Exlude forecasts groups that end with specified suffix "
"(for example, specify '-V9.10' for the csep-op server testing on a release date since models don't exist for the group yet). \
Default is None.")

    (values, args) = command_options.parse_args()
    #print 'OPTIONS', values
    
    CSEPWebTest.URL = values.top_level_url
    CSEPWebTest.Username = values.username
    CSEPWebTest.Password = values.userpass
    CSEPWebTest.ExcludeGroupSuffix = values.exclude_group_suffix


    suite = unittest.TestLoader().loadTestsFromTestCase(CSEPWebTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

   
    # Invoke all tests
    #unittest.main()
        
# end of main
