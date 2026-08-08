from app.prompting.roles import ask_as_role, ROLES

question = "Can you help me with derivatives in calculus?"

for role in ROLES:
    print(f"\n########## ROLE: {role.upper()} ##########")
    print(ask_as_role(role, question))