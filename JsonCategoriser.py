class IpondistributionSerialiser(object):
    """
    Takes in JSON object, splits into various parts, then convert to json
    1) CLIENT NAME/CAMPAIGN DETAILS
    2) CREATIVE
    3) TARGETING
    4) PRICING
    5) BUDGET
    6) CREATIVES FOR CAMPAIGN
    7) PIXELS
    8) DATA PROVIDERS
    """
    category = {}
    category['CATEGORY_CAMPAIGNDETAILS'] = {}
    category['CATEGORY_CREATIVE'] = {}
    category['CATEGORY_TARGETING'] = {}
    category['CATEGORY_PRICING'] = {}
    category['CATEGORY_BUDGET'] = {}
    category['CATEGORY_CREATIVEDETAILS'] = {}
    category['CATEGORY_PIXELS'] = {}
    category['CATEGORY_DATAPROVIDERS'] = {}
    category['CATEGORY_LINEITEM'] = {}

    campaign_details_fields = ['name','id','start_date','end_date']
    campaign_creative_fields = ['creative','id']
    campaign_lineitem_fields = ['id','name','start_date','end_date']
    campaign_targeting_fields = ['include','exclude','geo','networks','device_types', 'os_versions', 'device_models', 'browser_versions']
    # campaign_targeting_fields = ['geo','networks','browser_versions','device_models','device_types','inclusion','os_versions']
    campaign_pricing_fields = ['pricing_type','pricing_amount','pricing_optimisation','max_bid']
    campaign_budget_fields = ['budget','budget_pacing','daily_budget']
    campaign_creative_fields = ['name','id','creative_id','landing_page_url','type','can_track_clicks','size','bidswitch','html_content'] # NEEDS REFACORING TO JSON FIELDS
    campaign_pixel_fields = ['expiration_hours','pixel_name','pixel_id']    
    campaign_dataproviders_fields = ['data_provider_name','data_provider_targeting_label'] # NEEDS REFACTORING TO FINAL DUMMY JSON DATA

    def __init__(self,object):
        self.object = object


    @property
    def create_category_campaign_details(self):
        """
        Campaign category details
        check fields = 'name','id','start_date','end_date'

        Example:
        -categorise_json = IpondistributionSerialiser(object)
        -categorise_json.create_category_campaign_details

        Example Result:
        {CATEGORY_CAMPAIGNDETAILS:'id':'','name':'','start_date':'','end_date':''}

        """

        # *Confirm the placemet of this with Jose...This current take line item details
        for field in self.campaign_details_fields:
            try:
                advertiser_field = 'advertiser_' + str(field)
                fetch_advertiser_items = self.object['line_items'][0].get(field,None)
                self.category['CATEGORY_CAMPAIGN_DETAILS'][advertiser_field] = fetch_advertiser_items
            except:
                self.category['CATEGORY_CAMPAIGN_DETAILS'][advertiser_field] = None
            try:
                campaign_field = 'campaign_' + str(field)
                fetch_campaign_items = self.object.get(field,None)
                self.category['CATEGORY_CAMPAIGN_DETAILS'][campaign_field] = fetch_campaign_items
            except:
                self.category['CATEGORY_CAMPAIGN_DETAILS'][campaign_field] = None
        return self.category

    @property 
    def create_category_lineitem(self):
        """
        Create parent line item

        Example:
        -categorise_json = IpondistributionSerialiser(object)
        -categorise_json.create_category_lineitem

        Example Result:
        {CATEGORY_LINEITEM:'id':'','name':'','start_date':'','end_date':''}
        """
        for field in self.campaign_lineitem_fields:
            try:
                fetch_lineitem_items = self.object['line_items'][0].get(field,None)
                self.category['CATEGORY_LINEITEM'][field] = fetch_lineitem_items
            except:
                self.category['CATEGORY_LINEITEM'][field] = None
        return self.category



    @property
    def create_category_creative_parent(self):
        """
        Creative category details

        Example:
        -categorise_json = IpondistributionSerialiser(object)
        -categorise_json.create_category_creative_parent

        Example Result:
        {'CATEGORY_CREATIVE':'creative':'','id':''}

        """
        for field in self.campaign_creative_fields:
            try:
                fetch_creative_items = self.object['line_items'][0].get(field,None)
                self.category['CATEGORY_CREATIVE'][field] = fetch_creative_items
            except:
                self.category['CATEGORY_CREATIVE'][field] = None
        return self.category

    @property
    def create_category_targeting(self):
        """
        Targeting category details

        Example:
        -categorise_json = IpondistributionSerialiser(object)
        -categorise_json.create_catgeory_targeting

        Example Result:
        {'CATEGORY_TARGETING':'include':'','exlude':'','geo':'','networks':'','device_models':'','browser_versions':''}

        
        """
        base_case_platform = self.object['line_items'][0]['targeting_items']

        for seek_category in base_case_platform:
            test_existence = seek_category['config']
            for field_exists in self.campaign_targeting_fields:
                if field_exists in test_existence:
                    try:
                        grab_value = test_existence.get(field_exists,None)
                        self.category['CATEGORY_TARGETING'][field_exists] = grab_value
                    except:
                        self.category['CATEGORY_TARGETING'][field_exists] = None


        return self.category


    @property
    def create_category_pricing(self):
        """
        Pricing category fields
         Example:
        -categorise_json = IpondistributionSerialiser(object)
        -categorise_json.create_catgeory_pricing

        Example Result:
        {'CATEGORY_PRICING':'pricing_type':'','pricing_amount':'','pricing_optimisation':'','max_bid':''}

        """
        for field in self.campaign_pricing_fields:
            try:
                fetch_pricing_items = self.object['line_items'][0].get(field,None)
                self.category['CATEGORY_PRICING'][field] = fetch_pricing_items
            except:
                self.category['CATEGORY_PRICING'][field] = None
        return self.category

    @property
    def create_category_budget(self):
        """
        Budget category fields
         Example:
        -categorise_json = IpondistributionSerialiser(object)
        -categorise_json.create_catgeory_budget

        Example Result:
        {'CATEGORY_BUDGET':'budget':'','budget_pacing':'','daily_budget':''}

        """
        for field in self.campaign_budget_fields:
            try:
                fetch_budget_items = self.object['line_items'][0].get(field,None)
                self.category['CATEGORY_BUDGET'][field] = fetch_budget_items
            except:
                self.category['CATEGORY_BUDGET'][field] = None
        return self.category

    @property
    def create_category_creatives(self):
        """
        * Needs finalisation of json data
        Creatives category fields

        Example:
        -categorise_json = IpondistributionSerialiser(object)
        -categorise_json.create_catgeory_createives

        Example Result:
        {'CATEGORY_CREATIVE_DETAILS':'include':'','exlude':'','geo':'','networks':'','device_models':'','browser_versions':''}

        """

        for field in self.campaign_creative_fields:
            try:
                fetch_creative_items = self.object['creatives'][0].get(field,None)
                self.category['CATEGORY_CREATIVE_DETAILS'][field] = fetch_creative_items
            except:
                self.category['CATEGORY_CREATIVE_DETAILS'][field] = None
        return self.category

    @property
    def create_category_pixels(self):
        """
        * Needs finalisation of json data

        Pixels category fields
        Example:
        -categorise_json = IpondistributionSerialiser(object)
        -categorise_json.create_catgeory_pixels

        Example Result:
        {'CATEGORY_CREATIVE_PIXELS':'expiration_hours':'','pixel_name':'','pixel_id':''}

        """

        for field in self.campaign_pixel_fields:
            try:
                fetch_pixel_items = self.object['line_items'][0].get(field,None)
                self.category['CATEGORY_PIXELS'][field] = fetch_pixel_items
            except:
                self.category['CATEGORY_PIXELS'][field] = None
        return self.category

    @property
    def create_category_dataproviders(self):
        """
        Data providers category fields

         Example:
        -categorise_json = IpondistributionSerialiser(object)
        -categorise_json.create_category_dataproviders

        Example Result:
        {'CATEGORY_DATAPROVIDERS':'data_provider_name':'','data_provider_targeting_label':''}

        """

        for field in self.campaign_dataproviders_fields:
            try:
                fetch_pixel_items = self.object['line_items'][0].get(field,None)
                self.category['CATEGORY_PIXELS'][field] = fetch_pixel_items
            except:
                self.category['CATEGORY_PIXELS'][field] = None
        return self.category

    # return all functions


