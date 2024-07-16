from fastapi import APIRouter, Depends

from .schemas import GetRules_Body, CreateRules_Body, DeleteRules_Body
from ..dependencies import make_dependable
from ...database import Rule, rule_storage


router = APIRouter(prefix="/rules")


@router.get("/", response_model=list[Rule])
def get_rules(body: GetRules_Body = Depends(make_dependable(GetRules_Body))):
    return rule_storage.get(body.url, body.method)


@router.post("/", response_model=list[Rule])
def create_rules(rules_body: CreateRules_Body):
    rules = []
    for url in rules_body.urls:
        for method in rules_body.methods:
            rules.append(
                Rule(
                    url=url,
                    method=method,
                    refresh_rate=rules_body.refresh_rate,
                    requests=rules_body.requests,
                )
            )

    for rule in rules:
        rule_storage.save(rule)

    return rules


@router.delete("/", response_model=bool)
def delete_rule(body: DeleteRules_Body = Depends(make_dependable(DeleteRules_Body))):
    return rule_storage.delete(body.url, body.method)
