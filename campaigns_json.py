from lxml import etree
from Ipon import IponwebSerialiser
from iponweb_serialisers import TargetingItemIponwebSerialiser

class LineItemIponwebSerialiser(IponwebSerialiser):
    """
    Campaign focussed serialiser, producing categories:
    advertiser, campaign, lineitem, creative, pricing, budget
    """
    # each element appends up the tree
    root_element = etree.Element('config')

    @property
    def advertiser(self, ele, name):
        """
        <advertiser id='' name=''>

        """
        # Confirm this is correct-swap these details with line item details..
        node = etree.Element(name)

        advertiser_data = self.object['CATEGORY_CAMPAIGN_DETAILS']

        if isinstance(advertiser_data,dict):

                advertiser_fields = [
            {
                'src': 'advertiser_id',
                'dest': 'id',
                'value': advertiser_data['advertiser_id']
            },
            {
                'src': 'advertiser_name',
                'dest': 'name',
                'value': advertiser_data['advertiser_name']
            },
        ]

        # Add each of the pricing data to attr
        for field in advertiser_fields:
            self.field_to_attr(node, field)
            print self.field_to_attr(node, field)

        # Append new node to passed element
        ele.append(node)

        self.root_element.append(ele)
        # Test node
        # final_tree = etree.ElementTree(ele)
        # return etree.tostring(final_tree, pretty_print=True)

    def campaign(self, ele, name):
        """
        <campaign id="" name="">
        <start_date></start_date>
        <end_date></end_date>

        """
        # Need to append date to date_str function.....
        node = etree.Element(name)

        campaign_data = self.object['CATEGORY_CAMPAIGN_DETAILS']

        if isinstance(campaign_data,dict):

            campaign_fields = [
            {
                'src': 'campaign_id',
                'dest': 'id',
                'value': campaign_data['campaign_id']
            },
            {
                'src': 'campaign_name',
                'dest': 'name',
                'value': campaign_data['campaign_name']
            },
            {
                'src': 'campaign_start_date',
                'dest': 'start_date',
                'value': campaign_data['campaign_start_date']
            },
            {
                'src': 'campaign_end_date',
                'dest': 'end_date',
                'value': campaign_data['campaign_end_date']
            },
        ]

        for field in campaign_fields:
            # Call attach attribute function
            if field['src'] == 'campaign_id' or field['src'] =='campaign_name': 
                self.field_to_attr(node, field)
            # Call attach text function 
            if field['src'] == 'campaign_start_date' or field['src'] == 'campaign_end_date':
                dates_node = etree.Element(field['src'])
                self.field_to_node(dates_node, field)

        # Append new node to passed element
        ele.append(node)
        if dates_node.tag == 'campaign_start_date':
            node.append(dates_node)
        if dates_node.tag == 'campaign_end_date':
            node.append(dates_node)

        # Find tags in top root, then append to that if fits the criteria...
        # Test node
        final_tree = etree.ElementTree(ele)

        return etree.tostring(final_tree, pretty_print=True)

    def lineitem(self, ele, name):
        """
        Serialise to XML for LineItem items in json, approximately thus:

        <line_item id="129" name="Ford - Sep 2011">
          <start_date>2010-12-17 00:00:00</start_date>
          <end_date>2014-12-13 00:00:00</end_date>
          <targeting> ... </targeting>
          <creative> ... </creative>
          <pricing ... />
          <budget> ... </budget>
        </line_item>

        """
        node = etree.Element(name)

        lineitem_data = self.object['CATEGORY_LINEITEM']

        if isinstance(lineitem_data,dict):

            lineitem_fields = [
            {
                'src': 'id',
                'dest': 'id',
                'value': lineitem_data['id']
            },
            {
                'src': 'name',
                'dest': 'name',
                'value': lineitem_data['name']
            },
            {
                'src': 'start_date',
                'dest': 'start_date',
                'value': lineitem_data['start_date']
            },
            {
                'src': 'end_date',
                'dest': 'end_date',
                'value': lineitem_data['end_date']
            },
        ]


        for field in lineitem_fields:
            # Call attach attribute function
            if field['src'] == 'id' or field['src'] =='name': 
                self.field_to_attr(node, field)
            # Call attach text function 
            if field['src'] == 'start_date' or field['src'] == 'end_date':
                dates_node = etree.Element(field['src'])
                self.field_to_node(dates_node, field)

        # Append new node to passed element
        ele.append(node)
        if dates_node.tag == 'start_date':
            node.append(dates_node)
        if dates_node.tag == 'end_date':
            node.append(dates_node)

        # Append to campaign node.
        # Find tags in top root, then append to that if fits the criteria....
        newlineitem = self.root_element.find("campaign")
        if newlineitem.tag == 'campaign':
            newlineitem.append(ele)

        # Test node
        # final_tree = etree.ElementTree(ele)
        # return etree.tostring(final_tree, pretty_print=True)

    def creative(self, ele, name):
        """
        Simple foreignkey-ish representation of the creatives

        Node with name `name` will be added as child of `ele` and will have the
        following format:

        <ele>
            <creative>
                <value>1</value>
                <value>2</value>
            </creative>
        </ele>

        :param ele: Element to be adjusted - creatives will be added as child
            nodes
        :type ele: etree._Element
        :param name: Name for the node to be added, will be 'creative'
            according to current spec
        :type name: unicode, str
        """
        node = etree.Element(name)

        value_ids = list(str(self.object['CATEGORY_CREATIVE']['type']))

        try:
            for p_id in value_ids:
                value = etree.Element('value')
                value.text = str(p_id)
                node.append(value)

        except TypeError:
            value = etree.Element('value')
            value.text = str(None)
            node.append(value)

        ele.append(node)

        # Append to lineitem
        # Find tags in top root, then append to that if fits the criteria...
        newlineitem = self.root_element.find("line_item")
        if newlineitem.tag == 'line_item':
            newlineitem.append(ele)

        # Test Node
        # final_tree = etree.ElementTree(ele)

        # return etree.tostring(final_tree, pretty_print=True)

    def pricing(self, ele, name):
        """
        Uses pricing-related fields to construct pricing element

        Pricing node will be added as child node of `ele` like this (if there
        are all params found):

        <ele>
            <pricing type="CPM" amount="1.3" optimize="margin"/>
        </ele>

        If there are no params found then the self closing <pricing> tag will
        be added:

        <ele>
            <pricing/>
        </ele>

        :param ele: Element to be adjusted, pricing will be added as child node
        :type ele: etree._Element
        :param name: Name for the node to be added, will be 'pricing' according
            to current spec
        :type name: unicode, str
        """
        # TODO check what will happen if all none values are passed through,
        # should pricing node be created at all?

        # Config for pricing params

        # Create new node to hold pricing info
        node = etree.Element(name)

        pricing_data = self.object['CATEGORY_PRICING']

        if isinstance(pricing_data,dict):

            pricing_fields = [
            {
                'src': 'pricing_type',
                'dest': 'type',
                'value': pricing_data['pricing_type']
            },
            {
                'src': 'pricing_amount',
                'dest': 'amount',
                'value': pricing_data['pricing_amount']
            },
            {
                'src': 'pricing_optimisation',
                'dest': 'optimize',
                'value': pricing_data['pricing_optimisation']
            },
        ]

        # Add each of the pricing data to attrs
        for field in pricing_fields:
            self.field_to_attr(node, field)
            print self.field_to_attr(node, field)

        # Append new node to passed element
        ele.append(node)

        # Append to line item
        # Find tags in top root, then append to that if fits the criteria...
        newlineitem = self.root_element.find("line_item")
        if newlineitem.tag == 'line_item':
            newlineitem.append(ele)

        # Test node
        # final_tree = etree.ElementTree(ele)
        # return etree.tostring(final_tree, pretty_print=True)

    def budget(self, ele, name):
        """
        Uses budget-related fields to construct budget element

        If there are data field found, then a new node with tag `name` is
        inserted as a child of the passed `ele`.

        <ele>
            <budget>
                <pacing>asap</pacing>
                <daily_cap>100</daily_cap>
            </budget>
        </ele>

        If there is no budget data, then the node is not inserted under `ele`
        and False is returned.

        :param ele: Element to be adjusted, budget will be added as child node
        :type ele: etree._Element
        :param name: Name for the node to be added, will be 'budget' according
            to current spec
        :type name: unicode, str
        """
        # Config for budget

        budget_data = self.object['CATEGORY_BUDGET']

        budget_fields = (
            {
                'src': 'budget_pacing',
                'dest': 'pacing',
                'value': budget_data['budget_pacing']
            },
            {
                'src': 'daily_budget',
                'dest': 'daily_cap',
                'value': budget_data['daily_budget']
            },
        )

        # Create new node for budget
        node = etree.Element(name)

        # Call field to node for each budget param
        for field in budget_fields:
            self.field_to_node(node, field)

        # Kick out of no nodes were added to the budget node
        if len(node.getchildren()) == 0:
            return False

        # Otherwise all is good - append new budget node to passed element
        ele.append(node)

        # append to lineitem
        # Find tags in top root, then append to that if fits the criteria...
        newlineitem = self.root_element.find("line_item")
        if newlineitem.tag == 'line_item':
            newlineitem.append(ele)

        # final_tree = etree.ElementTree(ele)
        # return etree.tostring(final_tree, pretty_print=True)

    @property
    def xml(self):
        """Call parent xml func and then special functions"""
        # Build top level node for this object with attribs and nodes
        # root_element = super(LineItemIponwebSerialiser, self).xml

        # Call each special function with the name of the node it should create
        # under the root element
        fns = ['advertiser','lineitem','campaign','creative', 'pricing', 'budget']
        for fn_name in fns:
            # Currently all node names match their function name
            root_element = etree.Element(fn_name)
            getattr(self, fn_name)(root_element, fn_name)

        # Print parent root element.....

        final_tree = etree.ElementTree(self.root_element)

        return etree.tostring(final_tree, pretty_print=True)





