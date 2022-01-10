from api.datatype.Menu import Menu
from api.datatype.MenuCategory import MenuCategory
from api.datatype.MenuItem import MenuItem
from api.datatype.MenuItemSection import MenuItemSection
from api.datatype.MenuSubItem import MenuSubItem
from api.dfg.DfgNode import DfgNode
from api.datatype.Eatery import Eatery, EateryID
from eateries.models import MenuStore, CategoryItemAssociation, SubItemStore
# from eateries.models import DateEventSchedule

class CacheMenuInjection(DfgNode):

    def __init__(self, child: DfgNode, cache):
        self.cache = cache
        self.child = child

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        if "menus" not in self.cache:
            eatery_menus_categories_map = {}
            associations = CategoryItemAssociation.objects \
                .select_related("item") \
                .select_related("category") \
                .select_related("category__menu") \
                .all()
            
            subitems = SubItemStore.objects.all()
            item_subitem_map = {}
            for subitem in subitems:
                item_id = subitem.item_id
                item_subsection = subitem.item_subsection
                if item_id not in item_subitem_map:
                    item_subitem_map[item_id] = {}
                if item_subsection not in item_subitem_map[item_id]:
                    item_subitem_map[item_id][item_subsection] = []
                item_subitem_map[item_id][item_subsection].append(
                    MenuSubItem(
                        name=subitem.name, 
                        additional_price=subitem.additional_price, 
                        total_price=subitem.total_price
                    )
                )

            for association in associations:
                eatery_id = EateryID(association.category.menu.eatery_id)
                menu_id = association.category.menu_id
                category = association.category.category
                if eatery_id not in eatery_menus_categories_map:
                    eatery_menus_categories_map[eatery_id] = {}
                if menu_id not in eatery_menus_categories_map[eatery_id]:
                    eatery_menus_categories_map[eatery_id][menu_id] = {}
                if category not in eatery_menus_categories_map[eatery_id][menu_id]:
                    eatery_menus_categories_map[eatery_id][menu_id][category] = []
                item_sections = None
                if association.item.id in item_subitem_map:
                    item_sections = []
                    for section in item_subitem_map[association.item.id]:
                        item_sections.append(MenuItemSection(section, item_subitem_map[association.item.id][section]))

                eatery_menus_categories_map[eatery_id][menu_id][category].append(
                    MenuItem(
                        name = association.item.name,
                        healthy = None,
                        base_price = association.item.base_price,
                        description = association.item.description,
                        sections = item_sections
                    )
                )
            
            eatery_menus_map = {}
            for eatery_id in eatery_menus_categories_map:
                eatery_menus_map[eatery_id] = {}
                for menu_id in eatery_menus_categories_map[eatery_id]:
                    categories = []
                    for category in eatery_menus_categories_map[eatery_id][menu_id]:
                        categories.append(
                            MenuCategory(
                                category=category,
                                items = eatery_menus_categories_map[eatery_id][menu_id][category]
                            )
                        )
                    eatery_menus_map[eatery_id][menu_id] = Menu(
                        categories=categories
                    )
            self.cache["menus"] = eatery_menus_map
        return self.child(*args, **kwargs)

    def description(self):
        return "EateryStubs"
