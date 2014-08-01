"""
The rbx.bidding.serialisers package contains all the code specific to the
serialisation into the iponweb XML format

"""
from lxml import etree


class IponwebSerialiser(object):
    """
    A class that takes an object and provides methods for generating XML that
    describes the object according to a provided schema.

    Required attributes:
     - node_name: What the XML node in the `xml` property will be called

    Optional attributes:
    iponweb_required: Fields that are required by Iponweb's schema but are
                      nullable at our end
    attr_fields: .... Fields that should be added to the node as XML attributes
    node_fields: .... Fields that should be added to the node as children,
                      with their value in the body of the element

    Notes
    -----

    The `attr_fields` and `node_fields` attributes described above can either
    be lists of strings or dicts. This is to cater for Iponweb naming
    conventions and conversions which don't perfectly coincide with our own.
    Single string in either of these means, use this as the name in RBX and in
    the XML and do no conversion.

    For each list item, if it's of type:

    * str: Use this string as the name of the RBX object param, serialise it to
        XML with this string as the name for the node or attribute.

    * dict: Define each parameter for this attribute conversion. The only
        required value is 'src'. E.g.

            {
                'src': 'start_date',            # Source of data
                'dest': 'begin_date',           # Destination name in XML
                'converter': make_date_string,  # Function to do conversion
            }

        This will collect the value of the 'start_date' from the RBX object,
        run it through the `make_date_string` method and save the result in
        `begin_date` in the XML output. 'dest' and 'converter' do not need to
        be set.
    """
    node_name = None
    iponweb_required = []
    attr_fields = []
    node_fields = []

    def __init__(self, object):
        """
        Receive instance of model to be serialised
        """
        self.object = object

    @staticmethod
    def src_dest(field):
        """
        Return the appropriate source and destination pair for the field

        :param field: String name for the field required, or a full dict with
            configuration for this field.
        :type field: str or dict
        :raises: KeyError if dict is passed without an item with key 'src'.
        """

        print 'fetching src_dest'
        if isinstance(field, dict):
            try:
                return field['src'], field['dest'], field['value']
            except KeyError:
                return field['src'], field['src'], field['value']
        
        return field, field


    # def get_field_value(self, field):
    #     """
    #     Load field from model instance being serialised

    #     If attribute is not available, then pass back None

    #     """
    #     print 'get field value'
    #     try:
    #         # RETURN DICT VALUE
    #         # return getattr(self.object, field)
    #         return 
    #         # return self.object['CATEGORY_PRICING'].get(field,None)
    #     except AttributeError:
    #         return None



    def value_dest(self, field):
        """
        Load field value from model field

        :param field: Either name of field in both XML and model, or a dict
            which explicitly declares the mapping and or conversion required.
        :type field: dict or str
        :returns: Tuple of stringified and unicoded Value of field if found and
            name of XML destination for data. Or False, False if no data.
            Converter fn will be applied if passed.
        :raises: Exception if value is None and field is required by schema
        """

        print 'fetching value_dest'
        src, dest, attr_value = self.src_dest(field)



        # value = self.get_field_value(src)

        if attr_value is None:
            if src in self.iponweb_required:
                message = "{0} is required by Iponweb's schema.".format(src)
                raise Exception(message)
            else:
                return (False, False)

        # Attempt to convert the value and return it as unicode. Accept
        # KeyError because 'converter' might not be specified, TypeError
        # because field might be just a string not a dict.
        try:
            converter_fn = field['converter']
            return unicode(converter_fn(attr_value)), dest
        except (KeyError, TypeError):
            return unicode(attr_value), dest

    def field_to_attr(self, ele, field):
        """
        Add a field to an attribute of passed element

        :param ele: Element to be adjusted
        :type ele: etree._Element
        :param field: Either name of field in both XML and model, or a Tuple
            which does the mapping from object to XML
        :type field: Tuple or str
        :returns: False if no value is found, None on success
        :raises: Exception if value is None and field is required by schema
        """


        # Load up value and attribute name from model
        print 'fetching field_to_attr'
        print 'field =', field, '....'

        value, attr = self.value_dest(field)

        if value is False:
            return False, 'failed field_attr_method'

        ele.set(attr, value)

    def field_to_node(self, ele, field):
        """
        Add field's value as a new child node to the node passed

        :param ele: Element to be adjusted
        :type ele: etree._Element
        :param field: Either name of field in both XML and model, or a Tuple
            which does the mapping from object to XML
        :type field: Tuple or str
        :returns: False if no value is found, None on success
        :raises: Exception if value is None and field is required by schema
        """
        # Load up value and attribute name from model
        print 'running field to node'
        value, node_name = self.value_dest(field)

        print 'resulting items from value_dest_func',value,node_name

        if value is False:
            return False, 'failed field_to_node'

        node = etree.Element(node_name)
        node.text = value
        ele.append(node)

    @property
    def xml(self):
        """
        Build XML for all attributes and nodes defined, returns XML object

        :returns: Fully built XML tree object
        :return type: etree._Element
        """
        # Build the initial node
        print 'call IponwebSerialiser xml function'
        root = etree.Element(self.node_name)

        # Build XML for all attrs
        print 'building xml tree for all nodes'
        for field in self.attr_fields:
            self.field_to_attr(root, field)

        # Build XML for all nodes
        for field in self.node_fields:
            self.field_to_node(root, field)

        return root

    def to_xml_string(self, pretty_print=False):
        """
        Return XML value as a string

        NOTE Set to product Unicode formatted strings with XML declaration
        turned off
        """
        return etree.tostring(self.xml, pretty_print=pretty_print,
                              encoding=unicode)
