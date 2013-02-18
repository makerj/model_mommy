#coding: utf-8

from django.test import TestCase
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key, RecipeForeignKey
from model_mommy.timezone import now
from test.generic.models import Person, DummyNumbersModel, DummyBlankFieldsModel


class TestDefiningRecipes(TestCase):
    def setUp(self):
        self.recipe_attrs = {
          'name': 'John Doe',
          'nickname': 'joe',
          'age': 18,
          'bio': 'Someone in the crowd',
          'birthday': now().date(),
          'appointment': now(),
          'blog': 'http://joe.blogspot.com',
          'wanted_games_qtd': 4,
          'birth_time': now()
        }
        self.person_recipe = Recipe(
          Person,
          **self.recipe_attrs
        )

    def test_flat_model_make_recipe_with_the_correct_attributes(self):
        """
          A 'flat model' means a model without associations, like
          foreign keys, many to many and one to one
        """
        person = self.person_recipe.make()
        self.assertEqual(person.name, self.recipe_attrs['name'])
        self.assertEqual(person.nickname, self.recipe_attrs['nickname'])
        self.assertEqual(person.age, self.recipe_attrs['age'])
        self.assertEqual(person.bio, self.recipe_attrs['bio'])
        self.assertEqual(person.birthday, self.recipe_attrs['birthday'])
        self.assertEqual(person.appointment, self.recipe_attrs['appointment'])
        self.assertEqual(person.blog, self.recipe_attrs['blog'])
        self.assertEqual(person.wanted_games_qtd, self.recipe_attrs['wanted_games_qtd'])
        self.assertNotEqual(person.id, None)

    def test_flat_model_prepare_recipe_with_the_correct_attributes(self):
        person = self.person_recipe.prepare()
        self.assertEqual(person.name, self.recipe_attrs['name'])
        self.assertEqual(person.nickname, self.recipe_attrs['nickname'])
        self.assertEqual(person.age, self.recipe_attrs['age'])
        self.assertEqual(person.bio, self.recipe_attrs['bio'])
        self.assertEqual(person.birthday, self.recipe_attrs['birthday'])
        self.assertEqual(person.appointment, self.recipe_attrs['appointment'])
        self.assertEqual(person.blog, self.recipe_attrs['blog'])
        self.assertEqual(person.wanted_games_qtd, self.recipe_attrs['wanted_games_qtd'])
        self.assertEqual(person.id, None)

    def test_accepts_callable(self):
        r = Recipe(DummyBlankFieldsModel,
            blank_char_field = lambda: 'callable!!'
        )
        value = r.make().blank_char_field
        self.assertEqual(value, 'callable!!')

    def test_make_recipes_with_args(self):
        """
          Overriding some fields values at recipe execution
        """
        person = self.person_recipe.make(name='Guido', age=56)
        self.assertNotEqual(person.name, self.recipe_attrs['name'])
        self.assertEqual(person.name, 'Guido')

        self.assertNotEqual(person.age, self.recipe_attrs['age'])
        self.assertEqual(person.age, 56)

        self.assertEqual(person.nickname, self.recipe_attrs['nickname'])
        self.assertEqual(person.bio, self.recipe_attrs['bio'])
        self.assertEqual(person.birthday, self.recipe_attrs['birthday'])
        self.assertEqual(person.appointment, self.recipe_attrs['appointment'])
        self.assertEqual(person.blog, self.recipe_attrs['blog'])
        self.assertEqual(person.wanted_games_qtd, self.recipe_attrs['wanted_games_qtd'])
        self.assertNotEqual(person.id, None)

    def test_prepare_recipes_with_args(self):
        """
          Overriding some fields values at recipe execution
        """
        person = self.person_recipe.prepare(name='Guido', age=56)
        self.assertNotEqual(person.name, self.recipe_attrs['name'])
        self.assertEqual(person.name, 'Guido')

        self.assertNotEqual(person.age, self.recipe_attrs['age'])
        self.assertEqual(person.age, 56)

        self.assertEqual(person.nickname, self.recipe_attrs['nickname'])
        self.assertEqual(person.bio, self.recipe_attrs['bio'])
        self.assertEqual(person.birthday, self.recipe_attrs['birthday'])
        self.assertEqual(person.appointment, self.recipe_attrs['appointment'])
        self.assertEqual(person.blog, self.recipe_attrs['blog'])
        self.assertEqual(person.wanted_games_qtd, self.recipe_attrs['wanted_games_qtd'])
        self.assertEqual(person.id, None)

    def test_make_recipe_without_all_model_needed_data(self):
        person_recipe = Recipe(Person, name='John Doe')
        person = person_recipe.make()
        self.assertEqual('John Doe', person.name)
        self.assertTrue(person.nickname)
        self.assertTrue(person.age)
        self.assertTrue(person.bio)
        self.assertTrue(person.birthday)
        self.assertTrue(person.appointment)
        self.assertTrue(person.blog)
        self.assertTrue(person.wanted_games_qtd)
        self.assertTrue(person.id)

    def test_prepare_recipe_without_all_model_needed_data(self):
        person_recipe = Recipe(Person, name='John Doe')
        person = person_recipe.prepare()
        self.assertEqual('John Doe', person.name)
        self.assertTrue(person.nickname)
        self.assertTrue(person.age)
        self.assertTrue(person.bio)
        self.assertTrue(person.birthday)
        self.assertTrue(person.appointment)
        self.assertTrue(person.blog)
        self.assertTrue(person.wanted_games_qtd)
        self.assertFalse(person.id)


class TestExecutingRecipes(TestCase):
    """
      Tests for calling recipes defined in mommy_recipes.py
    """
    def test_model_with_foreign_key(self):
        dog = mommy.make_recipe('test.generic.dog')
        self.assertEqual(dog.breed, 'Pug')
        self.assertIsInstance(dog.owner, Person)
        self.assertNotEqual(dog.owner.id, None)

        dog = mommy.prepare_recipe('test.generic.dog')
        self.assertEqual(dog.breed, 'Pug')
        self.assertIsInstance(dog.owner, Person)
        self.assertNotEqual(dog.owner.id, None)

    def test_model_with_foreign_key_as_str(self):
        dog = mommy.make_recipe('test.generic.other_dog')
        self.assertEqual(dog.breed, 'Basset')
        self.assertIsInstance(dog.owner, Person)
        self.assertNotEqual(dog.owner.id, None)

        dog = mommy.prepare_recipe('test.generic.other_dog')
        self.assertEqual(dog.breed, 'Basset')
        self.assertIsInstance(dog.owner, Person)
        self.assertNotEqual(dog.owner.id, None)

    def test_make_recipe(self):
        person = mommy.make_recipe('test.generic.person')
        self.assertIsInstance(person, Person)
        self.assertNotEqual(person.id, None)

    def test_make_recipe_with_quantity_parameter(self):
        people = mommy.make_recipe('test.generic.person', _quantity=3)
        self.assertEqual(len(people), 3)
        for person in people:
            self.assertIsInstance(person, Person)
            self.assertNotEqual(person.id, None)

    def test_make_recipe_with_quantity_parameter_respection_model_args(self):
        people = mommy.make_recipe('test.generic.person', _quantity=3, name='Dennis Ritchie', age=70)
        self.assertEqual(len(people), 3)
        for person in people:
            self.assertEqual(person.name, 'Dennis Ritchie')
            self.assertEqual(person.age, 70)
    def test_prepare_recipe(self):
        person = mommy.prepare_recipe('test.generic.person')
        self.assertIsInstance(person, Person)
        self.assertEqual(person.id, None)

    def test_make_recipe_with_args(self):
        person = mommy.make_recipe('test.generic.person', name='Dennis Ritchie', age=70)
        self.assertEqual(person.name, 'Dennis Ritchie')
        self.assertEqual(person.age, 70)

    def test_prepare_recipe_with_args(self):
        person = mommy.prepare_recipe('test.generic.person', name='Dennis Ritchie', age=70)
        self.assertEqual(person.name, 'Dennis Ritchie')
        self.assertEqual(person.age, 70)

    def test_import_recipe_inside_deeper_modules(self):
        recipe_name = 'test.generic.tests.sub_package.person'
        person = mommy.prepare_recipe(recipe_name)
        self.assertEqual(person.name, 'John Deeper')

    def test_make_many_from_recipe(self):
        persons = mommy.make_many_from_recipe('test.generic.person')
        self.assertIsInstance(persons, list)
        self.assertEqual(len(persons), mommy.MAX_MANY_QUANTITY)
        for person in persons:
            self.assertIsInstance(person, Person)
            self.assertNotEqual(person.id, None)

    def test_make_many_from_recipe_with_specified_quantity(self):
        quantity = 2
        persons = mommy.make_many_from_recipe('test.generic.person', quantity=quantity)
        self.assertIsInstance(persons, list)
        self.assertEqual(len(persons), quantity)

    def test_make_many_with_model_args(self):
        persons = mommy.make_many_from_recipe('test.generic.person', name='Dennis Ritchie', age=70)
        for person in persons:
            self.assertEqual(person.name, 'Dennis Ritchie')
            self.assertEqual(person.age, 70)

class ForeignKeyTestCase(TestCase):
    def test_foreign_key_method_returns_a_recipe_foreign_key_object(self):
        number_recipe = Recipe(DummyNumbersModel,
            float_field = 1.6
        )
        obj = foreign_key(number_recipe)
        self.assertIsInstance(obj, RecipeForeignKey)

    def test_not_accept_other_type(self):
        with self.assertRaises(TypeError) as c:
            foreign_key(2)
        exception = c.exception
        self.assertEqual(exception.message, 'Not a recipe')

    def test_do_not_create_related_model(self):
        """
          It should not attempt to create other object when
          passing the object as argument
        """
        person = mommy.make_recipe('test.generic.person')
        self.assertEqual(Person.objects.count(), 1)
        mommy.make_recipe('test.generic.dog', owner=person)
        self.assertEqual(Person.objects.count(), 1)
        mommy.prepare_recipe('test.generic.dog', owner=person)
        self.assertEqual(Person.objects.count(), 1)

    def test_do_query_lookup_for_recipes_make_method(self):
        """
          It should not attempt to create other object when
          using query lookup syntax
        """
        dog = mommy.make_recipe('test.generic.dog', owner__name='James')
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(dog.owner.name, 'James')

    def test_do_query_lookup_for_recipes_prepare_method(self):
        """
          It should not attempt to create other object when
          using query lookup syntax
        """
        dog = mommy.prepare_recipe('test.generic.dog', owner__name='James')
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(dog.owner.name, 'James')
