# -*- coding: utf-8 -*-

"""
Tests of the software
"""
import isbnlib

from datetime import date, datetime, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User

from alessandria.models import (
    Language, BookCategory, BookSubCategory, BookAudience, Book, Reader, Profession, Author, Publisher, AppliNews
)
from alessandria.utils import IsbnUtils, MyString


class GenericTest(TestCase):
    def setUp(self):
        self.user = self.create_user()

    def create_book(self, inst_nb, title=None, isbn_nb=None):
        language = Language.objects.create(label='FR')
        category1 = BookCategory.objects.create(label="cat%s" % inst_nb)
        sub_category1 = BookSubCategory.objects.create(label="s_cat%s" % inst_nb, parent_category=category1)
        audience1 = BookAudience.objects.create(label="Children%s" % inst_nb)
        if not title:
            title="Hello world%s" % inst_nb
        book = Book(
            title=title,
            language = language,
            publish_date=datetime.today(),
            category = category1,
            sub_category = sub_category1,
            classif_mark="abc%s" % inst_nb,
            height=21,
            isbn_nb = isbn_nb
        )
        book.created_by = self.user
        book.created_on = datetime.today()
        book.save()
        book.audiences.add(audience1)
        book.authors.add(self.create_author(inst_nb))
        book.publishers.add(self.create_publisher(inst_nb))
        book.clean()
        book.save()
        return book
    
    def create_reader(self, inst_nb, first_name=None, last_name=None, profession=None):
        r = Reader()
        if not first_name:
            first_name = "fn%s" % inst_nb
        r.first_name = first_name
        if not last_name:
            last_name = "ln%s" % inst_nb
        r.last_name = last_name
        r.addr1 = "addr%s" % inst_nb
        r.zip = "%s" % inst_nb
        r.city = "city%s" % inst_nb
        r.country = "FR"
        r.inscription_date = datetime.today()
        r.birthday = '1971-03-24'
        if profession is None:
            profession = Profession(label='p%s' % inst_nb)
            profession.save()
        r.profession = profession
        r.sex = 'm'
        r.created_by = self.user
        r.created_on = datetime.today()
        r.clean()
        r.save()
        return r
    
    def create_author(self, inst_nb, first_name=None, last_name=None, alias=None):
        a = Author()
        if not first_name:
            first_name = "fn%s" % inst_nb
        a.first_name = first_name
        if not last_name:
            last_name = "ln%s" % inst_nb
        a.last_name = last_name
        a.country = 'FR'
        a.created_by = self.user
        a.created_on = datetime.today()
        a.clean()
        a.save()
        return a
    
    def create_publisher(self, inst_nb, name=None):
        p = Publisher()
        if not name:
            name = "n%s" % inst_nb
        p.name = name
        p.country = 'FR'
        p.created_by = self.user
        p.created_on = datetime.today()
        p.clean()
        p.save()
        return p
    
    def create_user(self, first_name='lucie', last_name='fer', username='luciefer', email='lucie@hell.com'):
        return User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)


class PublisherTest(GenericTest):
    def setUp(self):
        super(PublisherTest, self).setUp()

    def test_create(self):
        p = self.create_publisher(1, name='pub à')
        p_r = Publisher.objects.get(id=p.id)
        self.assertEqual('PUB À', p_r.name)
        
        self.assertIsNotNone(Publisher.objects.get_by_name('pub à'))
        self.assertIsNotNone(Publisher.objects.get_by_name('PUB À'))

    def test_search(self):
        p = self.create_publisher(1, name='éditions eyrolles')
        self.assertIsNotNone(Publisher.objects.search(name='éditions'))
        self.assertIsNotNone(Publisher.objects.search(name='eyrolles'))


class AuthorTest(GenericTest):
    def setUp(self):
        super(AuthorTest, self).setUp()

    def test_create(self):
        a = self.create_author(1, first_name='jean-marc', last_name='farà')

        a_r = Author.objects.get(id=a.id)
        self.assertEqual('Jean-Marc', a_r.first_name)
        self.assertEqual('FARÀ', a_r.last_name)

        self.assertIsNotNone(Author.objects.get_by_first_and_last_name('jean-marc', 'farà'))
        self.assertIsNotNone(Author.objects.get_by_first_and_last_name('JEAN-MARC', 'FARÀ'))

    def test_search(self):
        self.create_author(1, first_name='Georges Prosper', last_name='Remi', alias='Hergé')
        self.assertIsNotNone(Author.objects.search(name='Remi'))
        self.assertIsNotNone(Author.objects.search(name='Hergé'))


class BookTest(GenericTest):
    def setUp(self):
        super(BookTest, self).setUp()

    def tearDown(self):
        pass

    def test_create_update_book(self):
        # Test create
        b_count = Book.objects.count()
        title='la dolce vita del papà öttinger'
        b1 = self.create_book('1', title=title)
        self.assertEqual(Book.objects.count(), b_count + 1)
        self.assertEqual(title.capitalize(), b1.title)

        # Test update
        b_u = Book.objects.filter(id=b1.id).first()
        b_u.classif_mark = 'm_classif'
        b_u.save()
        self.assertTrue(len(Book.objects.filter(classif_mark='m_classif')) > 0)

    def test_isbn(self):
        b2 = self.create_book('2', isbn_nb='9783037680582')
        self.assertIsNot(b2, None)

        # Make sure we don't have an error 'isbn nb already exists' when updating
        b_u = Book.objects.filter(isbn_nb='9783037680582').first()
        b_u.save()
        
        b2.isbn_nb = 'wrong_isbn'
        with self.assertRaises(ValidationError):
            b2.save()

    def test_isbn_lib(self):
        """Ensure the isbnlib works but also show use cases"""
        self.assertIsNone(isbnlib.get_canonical_isbn('notisbn'))
        self.assertIsNone(isbnlib.get_canonical_isbn('345'))

        isbn_nb = '978-3-03768-058-2'
        self.assertTrue(isbnlib.is_isbn13(isbn_nb))
        self.assertEqual(isbnlib.get_canonical_isbn(isbn_nb), '9783037680582')
        isbn_meta = isbnlib.meta(isbn_nb)
        self.assertTrue(isbn_meta['Title'].startswith('The Tourist City Berlin'))
        self.assertIn('Braun', isbn_meta['Publisher'])
        self.assertIn('Jana Richter', isbn_meta['Authors'][0])
        self.assertEqual(isbn_meta['Language'].lower(), 'en')
        self.assertEqual(isbn_meta['Year'], '2010')

    def test_isbn_utils(self):
        self.assertEqual(IsbnUtils.get_isbn_nb_from_meta(isbnlib.meta('978-3-03768-058-2')), '9783037680582')

        self.assertEqual(IsbnUtils.author_unpack(''), ('', ''))
        self.assertEqual(IsbnUtils.author_unpack('Doe'), ('', 'Doe'))
        self.assertEqual(IsbnUtils.author_unpack('John Doe'), ('John', 'Doe'))
        self.assertEqual(IsbnUtils.author_unpack('John Henry Doe'), ('John Henry', 'Doe'))

    def test_search(self):
        self.create_book('1', title='My first book')
        self.assertIsNotNone(Book.objects.search(title='my first'))


class ReaderTest(GenericTest):
    def setUp(self):
        super(ReaderTest, self).setUp()

    def tearDown(self):
        pass

    def test_create(self):
        r = self.create_reader(1, first_name='jean-marc', last_name='pelè')

        r_r = Reader.objects.get(id=r.id)
        self.assertEqual('Jean-Marc', r_r.first_name)
        self.assertEqual('PELÈ', r_r.last_name)

        self.assertIsNotNone(Reader.objects.get_by_first_and_last_name('jean-marc', 'pelè'))
        self.assertIsNotNone(Reader.objects.get_by_first_and_last_name('JEAN-MARC', 'PELÈ'))   

    def test_search(self):
        self.create_reader(1, first_name='Marc', last_name='Schneider')
        self.assertIsNotNone(Reader.objects.search(last_name='schneid'))


class AppliNewsTest(GenericTest):
    def setUp(self):
        pass
    
    def test_create_and_list(self):
        n1 = AppliNews(publish_date=date.today() + timedelta(days=-1), news="Hello1")
        n1.save()
        n2 = AppliNews(publish_date=date.today(), news="Hello2")
        n2.save()
        self.assertEqual(AppliNews.objects.count(), 2)
        self.assertEqual(AppliNews.objects.get_last().news, "Hello2")
        n_future = AppliNews(publish_date=date.today() + timedelta(days=2), news="Hello future")
        n_future.save()
        self.assertEqual(AppliNews.objects.count(), 3)
        # Make sure we don't retrieve news that will be published in the future
        self.assertEqual(len(AppliNews.objects.list()), 2)
        self.assertEqual(AppliNews.objects.get_last().news, "Hello2")


class UtilsTest(TestCase):
    def test_my_string(self):
        self.assertIsNone(MyString.remove_accents(None))
        self.assertEqual("", MyString.remove_accents(""))
        self.assertEqual("Hello", MyString.remove_accents("Hello"))
        self.assertEqual("parentheses", MyString.remove_accents("parenthèses"))
        self.assertEqual("PARENTHESES", MyString.remove_accents("PARENTHÈSES"))
