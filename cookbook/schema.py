import graphene
from graphene_django import DjangoObjectType

from ingredients.models import Category, Ingredient
from ingredients.serializers import IngredientSerializer

from graphene_django.rest_framework.mutation import SerializerMutation


# class MyAwesomeMutation(SerializerMutation):
#     class Meta:
#         serializer_class = IngredientSerializer



class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")

class MyAwesomeMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        category = graphene.Int()
    ingredient = graphene.Field(IngredientType)
    @classmethod
    def mutate(cls, root, info, name, notes,category):
        ingredient = Ingredient.objects.create(
            category_id=category,
            name=name,
            notes=notes
        )
        return  MyAwesomeMutation(ingredient=ingredient)
        # ingredient = Ingredient.objecst.create(
        #
        # )

class Mutation(graphene.ObjectType):
    update_ingredient = MyAwesomeMutation.Field()


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None


schema = graphene.Schema(query=Query, mutation=Mutation)
