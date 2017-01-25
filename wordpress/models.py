"""
Copyright 2009-2010 Joshua Roesslein
"""

from .utils import parse_iso8601


class ResultSet(list):
    """
    A list of like object that holds results from the WordPress API query.
    """

    def __init__(self):
        super(ResultSet, self).__init__()

    def ids(self):
        return [item.id for item in self if hasattr(item, 'id')]


class Model(object):

    @classmethod
    def parse(cls, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError

    @classmethod
    def parse_list(cls, json_list):
        """
        Prase a list of JSON objects into a result set of model instances.
        """
        results = ResultSet()

        for obj in json_list:
            if obj:
                results.append(cls.parse(obj))

        return results

    def __repr__(self):
        state = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(state))


class Post(Model):
    """
    A WordPress post object.

    Arguments
    ---------

    date : datetime
        The date the object was published, in the site’s timezone.
    date_gmt : datetime
        The date the object was published, as GMT.
    guid : dict
        The globally unique identifier for the object.
    id : int
        Unique identifier for the object.
    link : str
        URL to the object.
    modified : datetime
        The date the object was last modified, in the site’s timezone.
    modified_gmt : datetime
        The date the object was last modified, as GMT.
    slug : str
        An alphanumeric identifier for the object unique to its type.
    status : str
        A named status for the object.
    type : str
        Type of Post for the object.
    password : str
        A password to protect access to the content and excerpt.
    title : dict
        The title for the object.
    content : dict
        The content for the object.
    author : int
        The ID for the author of the object.
    excerpt : dict
        The excerpt for the object.
    featured_media : int
        The ID of the featured media for the object.
    comment_status : str
        Whether or not comments are open on the object.
    ping_status : str
        Whether or not the object can be pinged.
    format : str
        The format for the object.
    meta : list
        Meta fields.
    sticky : bool
        Whether or not the object should be treated as sticky.
    template : str
        The theme file to use to display the object.
    categories : list
        The terms assigned to the object in the category taxonomy.
    tags : list
        The terms assigned to the object in the post_tag taxonomy.
    liveblog_likes : int
        The number of Liveblog Likes the post has.
    """

    @classmethod
    def parse(cls, json):
        post = cls()
        setattr(post, '_json', json)

        for k, v in json.items():
            if k in ['date', 'date_gmt', 'modified', 'modified_gmt']:
                setattr(post, k, parse_iso8601(v))
            else:
                setattr(post, k, v)

        return post
