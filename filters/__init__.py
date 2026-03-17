from loader import dp

from .is_regular_member import IsRegularMemberFilter

if __name__ == "filters":
    dp.filters_factory.bind(IsRegularMemberFilter)
