import graphene
from graphene_django.types import DjangoObjectType
from .models import Todo
from graphql_jwt.decorators import login_required
from django.contrib.auth.models import User

# Todo Type
class TodoType(DjangoObjectType):
    class Meta:
        model = Todo

# User Type
class UserType(DjangoObjectType):
    class Meta:
        model = User

# Get all Todos and Get one Todo
class Query(graphene.ObjectType):
    todos = graphene.List(TodoType, id=graphene.Int())
    
    @login_required
    def resolve_todos(self, info, id=None):
        user = info.context.user
        if id: 
            todo = Todo.objects.filter(id=id, user=user)
            if not todo.exists(): raise Exception("Todo not found or it does not belong to you")
            return list(todo)
        return Todo.objects.filter(isDone=False, user=user)

# Create Todo
class CreateTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)
    class Arguments:
        name = graphene.String(required=True)
    @login_required
    def mutate(self, info, name):
        user = info.context.user
        if user.is_anonymous: raise Exception("Not logged in! Please login now!")
        todo = Todo(user=user, name=name)
        todo.save()
        return CreateTodo(todo=todo)

#Update Todo
class UpdateTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        isDone = graphene.Boolean()
    @login_required
    def mutate(self, info, id, name=None, isDone=None):
        user = info.context.user
        todo = Todo.objects.get(id=id)
        if user != todo.user: raise Exception("It's not your TODO")
        if name: todo.name = name
        if isDone: todo.isDone = isDone
        todo.save()
        return UpdateTodo(todo=todo)

#Delete Todo
class DeleteTodo(graphene.Mutation):
    message = graphene.String()
    class Arguments:
        id = graphene.Int(required=True)
    @login_required
    def mutate(self, info, id):
        user = info.context.user
        todo = Todo.objects.get(id=id)
        if user != todo.user: raise Exception("It's not your TODO")
        todo.delete()
        return DeleteTodo(message=f"Todo is deleted: {id}")

#Create User
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String()
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)
    def mutate(self, info, username, password1, password2, email=None):
        if password1 != password2: raise Exception("Passwords are not matched!")
        user = User(username=username, email=email)
        user.set_password(password1)
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()
    create_user = CreateUser.Field()