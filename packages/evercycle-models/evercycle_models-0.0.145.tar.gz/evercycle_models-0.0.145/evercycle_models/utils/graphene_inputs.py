import graphene


class AddressInput(graphene.InputObjectType):
    street = graphene.String(required=True)
    secondary = graphene.String()
    city = graphene.String(required=True)
    state = graphene.String(required=True)
    country = graphene.String(required=True)
    postal_code = graphene.String(required=True)


class ContactInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=True)
