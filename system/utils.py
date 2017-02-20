import requests
import json


class Utils(object):
    def __init__(self):
        self.api_url = '%s/api/v1' % self.config['api_url']
        self.api_token = self.readConfig()['api_token']

    def readConfig(self):
        # Open Json File
        with open('settings/config.json', 'r') as json_data:
            return json.load(json_data)

    def __getRequest(self, path):
        return requests.get(self.api_url + path)

    def __postRequest(self, path, data):
        return requests.post(self.api_url + path, data, headers={'X-Cachet-Token': self.api_token})

    def __putRequest(self, path, data):
        return requests.put(self.api_url + path, data, headers={'X-Cachet-Token': self.api_token})

    def __delRequest(self, path):
        return requests.delete(self.api_url + path, headers={'X-Cachet-Token': self.api_token})

    def ping(self):
        return self.__getRequest('/ping')

    def getComponents(self):
        return self.__getRequest('/components')

    def getComponentsByID(self, c_id):
        return self.__getRequest('/components/%s' % c_id)

    def postComponents(self, name, status, **kwargs):
        """
        Create a new component.

        :param name: Name of the component
        :param status: Status of the component; 1-4
        :param description: (optional) Description of the component
        :param link: (optional) A hyperlink to the component
        :param order: (optional) Order of the component
        :param group_id: (optional) The group id that the component is within
        :param enabled: (optional)
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs['name'] = name
        kwargs['status'] = status
        return self.__postRequest('/components', kwargs)  #

    def putComponentsByID(self, c_id, **kwargs):
        """
        Updates a component.

        :param id: Component ID
        :param name: (optional) Name of the component
        :param status: (optional) Status of the component; 1-4
        :param link: (optional) A hyperlink to the component
        :param order: (optional) Order of the component
        :param group_id: (optional) The group id that the component is within
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__putRequest('/components/%s' % c_id, kwargs)

    def deleteComponentsByID(self, c_id):
        """Delete a component.

        :param id: Component ID
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__delRequest('/components/%s' % c_id)

    def getComponentsGroups(self):
        """

        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__getRequest('/components/groups')

    def getComponentsGroupsByID(self, c_id):
        """

        :param id: ID of the group you want to fetch
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__getRequest('/components/groups/%s' % c_id)

    def postComponentsGroups(self, name, **kwargs):
        """

        :param name: Name of the component group
        :param order: (optional) Order of the component group
        :param collapsed: (optional) Whether to collapse the group by default
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs['name'] = name
        return self.__postRequest('/components/groups', kwargs)

    def putComponentsGroupsByID(self, c_id, **kwargs):
        """

        :param id: Component group to update
        :param name: (optional) Name of the component group
        :param order: (optional) Order of the group
        :param collapsed: (optional) Whether to collapse the group by default
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__putRequest('/components/groups/%s' % c_id, kwargs)

    def deleteComponentsGroupsByID(self, c_id):
        """

        :param id: Component group to delete
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__getRequest('/components/groups/%s' % c_id)

    def getIncidents(self):
        """Return all incidents.

        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__getRequest('/incidents')

    def getIncidentsByID(self, i_id):
        """Returns a single incident.

        :param id: Incident ID
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__getRequest('/incidents/%s' % i_id)

    def postIncidents(self, name, message, status, visible, **kwargs):
        """Create a new incident.

        :param name: Name of the incident
        :param message: A message (supporting Markdown) to explain more.
        :param status: Status of the incident.
        :param visible: Whether the incident is publicly visible.
        :param component_id: (optional) Component to update.
        :param component_status: (optional) The status to update the given component with.
        :param notify: (optional) Whether to notify subscribers.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs['name'] = name
        kwargs['message'] = message
        kwargs['status'] = status
        kwargs['visible'] = visible
        return self.__postRequest('/incidents', kwargs)

    def putIncidentsByID(self, i_id, **kwargs):
        """

        :param id: ID of the incident to update.
        :param name: (optional) Name of the incident
        :param message: (optional) A message (supporting Markdown) to explain more.
        :param status: (optional) Status of the incident.
        :param visible: (optional) Whether the incident is publicly visible.
        :param component_id: (optional) Component to update.
        :param notify: (optional) Whether to notify subscribers.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__putRequest('/incidents/%s' % i_id, kwargs)

    def deleteIncidentsByID(self, i_id):
        """Delete an incident.

        :param id: Incident ID
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__delRequest('/incidents/%s' % i_id)

    def getMetrics(self):
        """Returns all metrics that have been setup.

        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__getRequest('/metrics')

    def postMetrics(self, name, suffix, description, default_value, **kwargs):
        """Create a new metric.

        :param name: Name of metric
        :param suffix: Measurments in
        :param description: Description of what the metric is measuring
        :param default_value: The default value to use when a point is added
        :param display_chart: (optional) Whether to display the chart on the status page
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs['name'] = name
        kwargs['suffix'] = suffix
        kwargs['description'] = description
        kwargs['default_value'] = default_value
        return self.__postRequest('/metrics', kwargs)

    def getMetricsByID(self, c_id):
        """Returns a single metric, without points.

        :param id: Metric ID
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__getRequest('/metrics/%s' % c_id)

    def deleteMetricsByID(self, c_id):
        """Delete a metric.

        :param id: Metric ID
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__delRequest('/metrics/%s' % c_id)

    def getMetricsPointsByID(self, c_id):
        """Return a list of metric points.

        :param id: Metric ID
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__getRequest('/metrics/%s/points' % c_id)

    def postMetricsPointsByID(self, c_id, value, **kwargs):
        """Add a metric point to a given metric.

        :param id: Metric ID
        :param value: Value to plot on the metric graph
        :param timestamp: Unix timestamp of the point was measured
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs['value'] = value
        return self.__postRequest('/metrics/%s/points' % c_id, kwargs)

    def deleteMetricsPointsByID(self, c_id, point_id):
        """Delete a metric point.

        :param id: Metric ID
        :param point_id: Metric Point ID
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__delRequest('/metrics/%s/points/%s' % (c_id, point_id))

    def getSubscribers(self):
        """Returns all subscribers.

        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__getRequest('/subscribers')

    def postSubscribers(self, email, **kwargs):
        """Create a new subscriber.

        :param email: Email address to subscribe
        :param verify: (optional) Whether to send verification email
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs['email'] = email
        return self.__postRequest('/subscribers', kwargs)

    def deleteSubscribersByID(self, c_id):
        """Delete a subscriber.

        :param id: ID of the subscriber to delete
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__delRequest('/subscribers/%s' % c_id)
