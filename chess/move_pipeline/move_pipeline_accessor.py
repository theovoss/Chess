class MovePipelineAccessor():
    @staticmethod
    def get_attributes(scope, attributes, ignore=None):
        if not ignore:
            ignore = []
        return [getattr(scope, condition) for condition in attributes if hasattr(scope, condition) and condition not in ignore]
