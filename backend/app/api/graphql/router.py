from fastapi import APIRouter
from starlette_graphene3 import GraphQLApp

from .schema import schema

router = APIRouter()
router.add_route("/api/v1/graphql", GraphQLApp(schema=schema))
