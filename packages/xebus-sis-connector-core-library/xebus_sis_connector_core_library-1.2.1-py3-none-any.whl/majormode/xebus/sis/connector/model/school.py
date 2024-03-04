# Copyright (C) 2024 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from __future__ import annotations

import collections
from uuid import UUID

from majormode.perseus.constant.contact import ContactName
from majormode.perseus.constant.obj import ObjectStatus
from majormode.perseus.model.contact import Contact
from majormode.perseus.utils import cast
from majormode.perseus.utils.rdbms import RdbmsConnection
from majormode.xebus.constant.guardian import GuardianRole

from majormode.xebus.sis.connector.model.child import Child
from majormode.xebus.sis.connector.model.grade import EducationGrade
from majormode.xebus.sis.connector.model.guardian import Guardian, Guardianship
from majormode.xebus.sis.connector.model.school_class import SchoolClass


class SchoolDatabase:
    @staticmethod
    def __build_children_cache(children: list[Child]) -> dict[UUID | str, Child]:
        """
        Build the cache of a list of children with their Xebus and SIS identifiers.


        :param children: A list of children.


        :return: A dictionary of children indexed with their Xebus and SIS
            identifiers.
        """
        children_cache = {}

        for child in children:
            children_cache[child.account_id] = child
            children_cache[child.sis_account_id] = child

        return children_cache

    @staticmethod
    def __build_education_grades_cache(education_grades: list[EducationGrade]) -> dict[str, EducationGrade]:
        """
        Build the cache of a list of education grades with their names.


        :param education_grades: A list of education grades.


        :return: A dictionary of education grades indexed with their names.
        """
        education_grades_cache = {}

        for education_grade in education_grades:
            education_grades_cache[education_grade.grade_name] = education_grade
            education_grades_cache[education_grade.grade_level] = education_grade
            if education_grade.grade_short_name:
                education_grades_cache[education_grade.grade_short_name] = education_grade

        return education_grades_cache

    @staticmethod
    def __build_guardians_cache(guardians: list[Guardian]) -> dict[UUID | str, Guardian]:
        """
        Index a list of parents with their Xebus and SIS identifiers, their
            email address, and their phone number.


        :param guardians: A list of guardians.


        :return: A dictionary of guardian indexed with their Xebus and SIS
            identifiers, their email address, and their phone number.
        """
        guardians_cache = {}

        for guardian in guardians:
            guardians_cache[guardian.sis_account_id] = guardian

            if guardian.account_id:
                guardians_cache[guardian.account_id] = guardian

            if guardian.email_address:
                guardians_cache[guardian.email_address] = guardian

            if guardian.phone_number:
                guardians_cache[guardian.phone_number] = guardian

        return guardians_cache

    @staticmethod
    def __build_school_classes_cache(school_classes: list[SchoolClass]) -> dict[UUID | str, SchoolClass]:
        """
        Build the cache of a list of school classes with their identifier and
        their name.


        :param school_classes: A list of school classes.


        :return: A dictionary of school classes indexed with their identifier
            and their name.
        """
        school_classes_cache = {}

        for school_class in school_classes:
            school_classes_cache[school_class.class_id] = school_class
            school_classes_cache[school_class.class_name] = school_class

        return school_classes_cache

    @staticmethod
    def __fetch_children(
            school_id: UUID,
            guardians: list[Guardian],
            connection: RdbmsConnection
    ) -> list[Child]:
        """
        Return the list of children enrolled in the specified school.


        :param school_id: The identifier of a school.

        :param guardians: The list of the children's guardians.  The objects
            representing these parents will be referenced in the children's
            guardianships.

        :param connection: A connection to the family database.


        :return: A list of children enrolled in the specified school.
        """
        with connection:
            # Fetch the children's data.
            cursor = connection.execute(
                '''
                SELECT
                    account_id,
                    dob,
                    first_name,
                    full_name,
                    grade_level,
                    language,
                    last_name,
                    nationality,
                    ref AS sis_account_id
                  FROM
                    child
                  WHERE
                    school_id = %(school_id)s
                    AND object_status <> %(OBJECT_STATUS_DELETED)s
                ''',
                {
                    'OBJECT_STATUS_DELETED': ObjectStatus.deleted,
                    'school_id': school_id,
                }
            )

            records = [
                row.get_object({
                    'account_id': cast.string_to_uuid,
                    'language': cast.string_to_locale,
                })
                for row in cursor.fetch_all()
            ]

            for record in records:
                if record.account_id is None:
                    raise ValueError(
                        f"The identifier of the child \"{record.full_name}\" with SIS ID "
                        f"\"{record.sis_account_id}\" is undefined "
                    )

            children_dict: dict[UUID, Child] = {
                record.account_id: Child(
                    record.sis_account_id,
                    record.first_name,
                    record.last_name,
                    record.full_name,
                    record.dob,
                    record.grade_level,
                    account_id=record.account_id,
                    languages=record.language,
                    nationalities=record.nationality
                )
                for record in records
            }

            # Fetch the children's guardianships.
            cursor = connection.execute(
                '''
                SELECT
                    guardian_child.child_account_id,
                    guardian_child.guardian_account_id,
                    place_address.property_value AS home_address,
                    guardian_child.role
                  FROM
                    child
                  INNER JOIN guardian_child
                    ON (guardian_child.child_account_id = child.account_id)
                  LEFT JOIN place_address
                    ON (
                      place_address.place_id = guardian_child.home_id
                      AND place_address.account_id IS NULL                    
                      AND place_address.property_name = 'formatted_address'
                    )
                  WHERE
                    child.school_id = %(school_id)s
                    AND child.object_status <> %(OBJECT_STATUS_DELETED)s
                    AND guardian_child.object_status <> %(OBJECT_STATUS_DELETED)s
                ''',
                {
                    'OBJECT_STATUS_DELETED': ObjectStatus.deleted,
                    'school_id': school_id,
                }
            )

            records = [
                row.get_object({
                    'child_account_id': cast.string_to_uuid,
                    'guardian_account_id': cast.string_to_uuid,
                    'role': GuardianRole,
                })
                for row in cursor.fetch_all()
            ]

            guardians_dict = {
                guardian.account_id: guardian
                for guardian in guardians
            }

            children_guardianships = collections.defaultdict(list)
            for record in records:
                guardian = guardians_dict[record.guardian_account_id]
                if not guardian:
                    raise ValueError(
                        f'No guardian found in the school database with the identifier "{record.guardian_account_id}"'
                    )

                children_guardianships[record.child_account_id].append(
                    Guardianship(guardian, record.role, record.home_address)
                )

            for child_account_id in children_dict:
                child_guardianships = children_guardianships[child_account_id]
                for child_guardianship in child_guardianships:
                    children_dict[child_account_id].add_guardianship(child_guardianship)

        return list(children_dict.values())

    @classmethod
    def __fetch_guardians(
            cls,
            school_id: UUID,
            connection: RdbmsConnection
    ) -> list[Guardian]:
        """
        Return the list of parents whose children are enrolled in the
        specified school.


        :param school_id: The identifier of the school that the parents'
            children are enrolled in.

        :param connection: A connection to the family database.


        :return: The list of parents whose children are enrolled in the
            specified school.
        """
        with connection:
            # Fetch the list of parents whose children are registered to the
            # specified school.
            cursor = connection.execute(
                '''
                SELECT
                    account_id,
                    first_name,
                    full_name,
                    language,
                    last_name,
                    nationality,
                    ref AS sis_account_id
                  FROM
                    account
                  WHERE
                    account_id IN (
                      SELECT DISTINCT
                          guardian_child.guardian_account_id
                        FROM
                          child
                        INNER JOIN guardian_child
                          ON (
                            guardian_child.child_account_id = child.account_id
                          )
                        WHERE
                          child.school_id = %(school_id)s
                    )
                    AND object_status <> %(OBJECT_STATUS_DELETED)s
                ''',
                {
                    'OBJECT_STATUS_DELETED': ObjectStatus.deleted,
                    'school_id': school_id,
                }
            )

            records = [
                row.get_object({
                    'account_id': cast.string_to_uuid,
                    'language': cast.string_to_locale,
                })
                for row in cursor.fetch_all()
            ]

        # Fetch the contact information of the parents.
        parent_ids = [record.account_id for record in records]
        if not parent_ids:
            return []

        parents_contacts = cls.__fetch_verified_primary_contacts(parent_ids, connection)

        # Build the list of the parents with their respective contact
        # information.
        parents = [
            Guardian(
                record.sis_account_id,
                record.first_name,
                record.last_name,
                record.full_name,
                account_id=record.account_id,
                contacts=parents_contacts[record.account_id],
                languages=record.language,
                nationalities=record.nationality
            )
            for record in records
        ]

        return parents

    @staticmethod
    def __fetch_guardianships(
            children: list[Child],
            parents: list[Child],
            connection: RdbmsConnection
    ) -> None:
        """
        Fetch and build the guardianships of the specified children.

        The function builds a new object {@link Guardianship} representing the
        guardianship with a parent and adds this object to the corresponding
        child object.


        :param children: A list of children to return their parents

        :param parents: A list of parents who are registered as the legal
            guardians of these children.

        :param connection: A connection to the family database.
        """
        # Fetch the list of guardianships of the children.
        child_ids = [child.account_id for child in children]

        with connection:
            cursor = connection.execute(
                '''
                SELECT
                    child_account_id,
                    guardian_account_id,
                    home_id,
                    role
                  FROM
                    guardian_child
                  WHERE 
                    child_account_id IN (%(account_ids)s)
                    AND object_status <> %(OBJECT_STATUS_DELETED)s
                ''',
                {
                    'OBJECT_STATUS_DELETED': ObjectStatus.deleted,
                    'account_ids': child_ids,
                }
            )

            records = [
                row.get_object({
                    'child_account_id': cast.string_to_uuid,
                    'guardian_account_id': cast.string_to_uuid,
                    'home_id': cast.string_to_uuid,
                    'role': GuardianRole
                })
                for row in cursor.fetch_all()
            ]

        # Indexes the children and the parents with their respective account
        # identification for faster access.
        children_dict = {
            child.account_id: child
            for child in children
        }

        parents_dict = {
            parent.account_id: parent
            for parent in parents
        }

        for record in records:
            children_dict[record.child_account_id].add_guardianship(
                Guardianship(parents_dict[record.guariand_account_id], record.role)
            )

    @staticmethod
    def __fetch_school_classes(
            school_id: UUID,
            connection: RdbmsConnection
    ) -> list[SchoolClass]:
        """
        Return the list of the classes of a school.


        :param school_id: The identifier of the school to return the list of
            classes.

        :param connection: A connection to the school database.


        :return: The list of the school's classes.
        """
        with connection:
            cursor = connection.execute(
                '''
                SELECT
                    class_id,
                    get_class_name(class_id) AS class_name,
                    creation_time,
                    end_date,
                    grade_level_max,
                    grade_level_min,
                    start_date,
                    update_time
                  FROM
                    school_class
                  WHERE
                    school_id = %(school_id)s
                    AND current_date BETWEEN start_date AND end_date
                    AND object_status = %(OBJECT_STATUS_ENABLED)s
                ''',
                {
                    'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                    'school_id': school_id,
                }
            )

            records = [
                row.get_object({
                    'class_id': cast.string_to_uuid,
                    'creation_time': cast.string_to_timestamp,
                    'update_time': cast.string_to_timestamp,
                })
                for row in cursor.fetch_all()
            ]

            school_classes = [
                SchoolClass(
                    record.class_id,
                    record.class_name,
                    record.grade_level_min,
                    record.grade_level_max,
                    record.start_date,
                    record.end_date
                )
                for record in records
            ]

            return school_classes

    @staticmethod
    def __fetch_school_education_grades(
            school_id: UUID,
            connection: RdbmsConnection
    ) -> list[EducationGrade]:
        """
        Return the list of the education grades that a school offers to their
        pupils.


        :todo: Reuse the EducationService.

        :todo: The current implementation implies that the education grades of
            a school depends on the standard education grades of a country,
            while some school organizations may have used their own education
            grades.


        :param school_id: The identifier of a school.

        :param connection: A connection to the school database.


        :return: A list of the education grades of the school:

            - ``end_age: int`` (required): The age at which pupils usually complete
              this grade level.

            - ``grade_level: int`` (required): The number of the year that pupils
              have spent in the school’s education level to reach this grade level.
              Starts from ``0``.

            - ``grade_name: str`` (required): The name given to this grade level.

            - ``grade_short_name: str`` (optional): The short name given to this
               grade level.

            - ``start_age: int`` (required): The age at which pupils usually start
              this grade level.
        """
        with connection:
            cursor = connection.execute(
                '''
                SELECT
                     end_age,
                     grade_level,
                     grade_name,
                     grade_short_name,
                     start_age
                  FROM
                    education_grade
                  WHERE
                    country_code = (
                      SELECT
                          country_code
                        FROM
                          school
                        WHERE
                          place_id = %(school_id)s
                    )
                ''',
                {
                    'school_id': school_id,
                }
            )

            records = [
                row.get_object()
                for row in cursor.fetch_all()
            ]

            education_grades = [
                EducationGrade(
                    record.grade_level,
                    record.grade_name,
                    record.start_age,
                    record.end_age,
                    grade_short_name=record.grade_short_name,
            )
                for record in records
            ]

            return education_grades

    @staticmethod
    def __fetch_verified_primary_contacts(
            account_ids: list[UUID],
            connection: RdbmsConnection
    ) -> dict[UUID, list[Contact]]:
        """
        Fetch the contacts of parents.

        The function only returns primary contacts that have been verified.


        :param account_ids: The identifier of the parents to fetch the
            contact information.


        :return: A dictionary-like object where the key corresponds to the
            identifier of a parent, and the value corresponds to the list
            of the contact information of this parent.
        """
        if not account_ids:
            return {}

        with connection:
            cursor = connection.execute(
                '''
                SELECT
                    account_id,
                    property_name,
                    property_value
                  FROM
                    account_contact
                  WHERE
                    account_id IN (%(account_ids)s)
                    AND is_primary = true
                    AND is_verified = true
                ''',
                {
                    'account_ids': account_ids,
                }
            )

            records = [
                row.get_object({
                    'account_id': cast.string_to_uuid,
                    'property_name': ContactName,
                })
                for row in cursor.fetch_all()
            ]

        parents_contacts = collections.defaultdict(list)
        for record in records:
            parents_contacts[record.account_id].append(
                Contact(
                    record.property_name,
                    record.property_value,
                    is_primary=True,
                    is_verified=True
                )
            )

        return parents_contacts

    def __init__(
            self, school_id: UUID,
            children: list[Child],
            guardians: list[Guardian],
            education_grades: list[EducationGrade],
            school_classes: list[SchoolClass],
    ):
        """
        Build an object representing a school's database.


        :param school_id: The school's identifier.

        :param children: The list of children enrolled in this school.

        :param guardians: The list of the guardians of these children.

        :param education_grades: The list of education grades that the school
            offers.

        :param school_classes: The list of the school's classes for the
            current or coming school year.
        """
        self.__school_id = school_id

        self.__education_grades = education_grades
        self.__education_grades_cache = self.__build_education_grades_cache(education_grades)

        self.__school_classes = school_classes
        self.__school_classes_cache = self.__build_school_classes_cache(school_classes)

        self.__children = children
        self.__children_cache = self.__build_children_cache(children)

        self.__guardians = guardians
        self.__guardians_cache = self.__build_guardians_cache(guardians)

    @classmethod
    def build_school_database(
            cls,
            connection: RdbmsConnection,
            school_id: UUID
    ) -> SchoolDatabase:
        """
        Build an object representing the data of a school.


        :param connection: A connection to the school database.

        :param school_id: The identifier of a school.


        :return: The school's database.
        """
        school_classes = cls.__fetch_school_classes(school_id, connection)
        education_grades = cls.__fetch_school_education_grades(school_id, connection)
        guardians = cls.__fetch_guardians(school_id, connection)
        children = cls.__fetch_children(school_id, guardians, connection)

        school_database = SchoolDatabase(
            school_id,
            children,
            guardians,
            education_grades,
            school_classes
        )

        return school_database

    def find_child(self, sis_account_id: str) -> Child | None:
        """
        Return the child object stored in the database.


        :param sis_account_id: The SIS identifier of a child.


        :return: The child object stored in the database, if any found.
        """
        return self.__children_cache.get(sis_account_id)

    def find_education_grade(self, grade_name_or_level: str | int) -> EducationGrade | None:
        """
        Return the education grade corresponding to the specified name or
        level.


        :param grade_name_or_level: The name or level of an education grade.


        :return: The education grade corresponding to the specified name or
            level, if any found.
        """
        return grade_name_or_level and self.__education_grades_cache.get(grade_name_or_level)

    def find_guardian(self, identifier: UUID | str) -> Guardian | None:
        return identifier and self.__guardians_cache.get(identifier)

    def find_school_class(self, identifier: UUID | str | None) -> SchoolClass | None:
        return identifier and self.__school_classes_cache.get(identifier)

    # def find_parent_with_email_address(self, connection: RdbmsConnection, email_address: str) -> Guardian | None:
    #     with connection:
    #         cursor = connection.execute(
    #             '''
    #             SELECT
    #                 account_id
    #               FROM
    #                 account_contact
    #               WHERE
    #                 property_name = %(CONTACT_NAME_EMAIL)s
    #                 AND property_value = %(email_address)s
    #                 AND is_primary = true
    #                 AND is_verified = true
    #                 AND object_status <> %(OBJECT_STATUS_DELETED)s
    #             ''',
    #             {
    #                 'CONTACT_NAME_EMAIL': ContactName.EMAIL,
    #                 'OBJECT_STATUS_DELETED': ObjectStatus.deleted,
    #                 'email_address': email_address,
    #                 'school_id': self.__school_id,
    #             }
    #         )
    #
    #         row = cursor.fetch_one()
    #         if not row:
    #             return None
    #
    #         account_id = row.get_value('account_id', cast.string_to_uuid)
    #         return self.__fetch_parent(account_id)
    #
    # def find_parent_with_sis_id(self, connection: RdbmsConnection, sis_account_id: str) -> Guardian | None:
    #     """
    #     Return the guardian object stored in the database.
    #
    #
    #     :param sis_account_id: The SIS identifier of a parent.
    #
    #
    #     :return: The guardian object stored in the database, if any found.
    #     """
    #     with self.__connection as connection:
    #         cursor = connection.execute(
    #             '''
    #             SELECT
    #                 account_id
    #               FROM
    #                 account
    #               WHERE
    #                 sis_account_id = %(sis_account_id)s
    #                 AND school_id = %(school_id)s
    #                 AND object_status <> %(OBJECT_STATUS_DELETED)s
    #             ''',
    #             {
    #                 'OBJECT_STATUS_DELETED': ObjectStatus.deleted,
    #                 'school_id': self.__school_id,
    #                 'sis_account_id': sis_account_id,
    #             }
    #         )
    #
    #         row = cursor.fetch_one()
    #         if not row:
    #             return None
    #
    #         account_id = row.get_value('account_id', cast.string_to_uuid)
    #         return self.__fetch_parent(account_id)

    # def has_child(self, child: Child) -> bool:
    #     registered_child = self.find_child(child)
    #     return registered_child is not None
    #
    # def has_guardian(self, guardian: Guardian) -> bool:
    #     registered_guardian = self.find_parent(guardian)
    #     return registered_guardian is not None
