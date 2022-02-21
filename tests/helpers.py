from xmatters import utils


def assert_attrs_for_data(iterable):
    for i in iterable:
        if i:
            for k in i._api_data.keys():
                snake_k = utils.camel_to_snakecase(k)
                assert hasattr(i, snake_k)


def all_types_in_factory(iterable, factory):
    type_attr = utils.snake_to_camelcase(factory._id_attr)
    for i in iterable:
        if i:
            assert i._api_data.get(type_attr) in factory._factory_objects.keys()
