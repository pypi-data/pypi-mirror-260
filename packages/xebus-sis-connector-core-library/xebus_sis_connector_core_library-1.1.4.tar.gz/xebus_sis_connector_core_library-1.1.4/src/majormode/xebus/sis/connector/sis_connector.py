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

import abc
import datetime
import logging
import string
from abc import ABC
from typing import Any

from dateutil.parser import ParserError
from majormode.perseus.constant.contact import ContactName
from majormode.perseus.model.contact import Contact
from majormode.perseus.utils import cast

from majormode.xebus.sis.connector.constant.family import FamilyPropertyName
from majormode.xebus.sis.connector.constant.vendor import SisVendor
from majormode.xebus.sis.connector.model.family import FamilyList


class SisConnector(ABC):
    # Declare the list of property names for a child.
    CHILD_PROPERTY_NAMES = [
        FamilyPropertyName.child_sis_id,
        FamilyPropertyName.child_first_name,
        FamilyPropertyName.child_last_name,
        FamilyPropertyName.child_full_name,
        FamilyPropertyName.child_languages,
        FamilyPropertyName.child_nationalities,
        FamilyPropertyName.child_date_of_birth,
        FamilyPropertyName.child_grade_level,
        FamilyPropertyName.child_class_name,
        FamilyPropertyName.child_use_transport,
    ]

    # Declare the list of the property names for a primary guardian.
    PRIMARY_GUARDIAN_PROPERTY_NAMES = [
        FamilyPropertyName.primary_guardian_sis_id,
        FamilyPropertyName.primary_guardian_first_name,
        FamilyPropertyName.primary_guardian_last_name,
        FamilyPropertyName.primary_guardian_full_name,
        FamilyPropertyName.primary_guardian_languages,
        FamilyPropertyName.primary_guardian_nationalities,
        FamilyPropertyName.primary_guardian_email_address,
        FamilyPropertyName.primary_guardian_phone_number,
        FamilyPropertyName.primary_guardian_home_address,
    ]

    # Declare the list of the property names for a secondary guardian.
    #
    # :note: The secondary guardian's property names MUST be declared in
    #     exactly the same order as those of the primary guardian.
    SECONDARY_GUARDIAN_PROPERTY_NAMES = [
        FamilyPropertyName.secondary_guardian_sis_id,
        FamilyPropertyName.secondary_guardian_first_name,
        FamilyPropertyName.secondary_guardian_last_name,
        FamilyPropertyName.secondary_guardian_full_name,
        FamilyPropertyName.secondary_guardian_languages,
        FamilyPropertyName.secondary_guardian_nationalities,
        FamilyPropertyName.secondary_guardian_email_address,
        FamilyPropertyName.secondary_guardian_phone_number,
        FamilyPropertyName.secondary_guardian_home_address,
    ]

    assert len(PRIMARY_GUARDIAN_PROPERTY_NAMES) == len(SECONDARY_GUARDIAN_PROPERTY_NAMES), \
        "Primary guardian's property list is not the same as secondary " \
        "guardian's property list"

    def __init__(
            self,
            vendor: SisVendor
    ):
        self.__vendor = vendor

    def _cleanse_rows(
            self,
            rows: list[dict[FamilyPropertyName, Any]]
    ) -> list[dict[FamilyPropertyName, Any]]:
        """
        Cleanse the family list from unexpected conditions.

        If a secondary guardian is declared without a required identifier,
        such as an email address, their information will be cleared.  As a
        result, this secondary guardian will be ignored during the
        synchronization process.

        If a primary guardian is declared without a required identifier, they
        will be replaced with the secondary guardian.


        :param rows: The family list to clear.


        :return: The family list with the rows cleansed.


        :raise ValueError: If a child is declared with guardians without a
            defined email address.
        """
        for row_index, row in enumerate(rows):
            # If the secondary guardian is not declared with an email address, we
            # clear their information from this row.
            if not cast.is_undefined(row[FamilyPropertyName.secondary_guardian_sis_id]) \
               and cast.is_undefined(row[FamilyPropertyName.secondary_guardian_email_address]):
                logging.warning(
                    f"The secondary guardian \"{row[FamilyPropertyName.secondary_guardian_sis_id]} "
                    "is not declared with an email address; clearing their information..."
                )
                self._clear_row_properties(row, self.SECONDARY_GUARDIAN_PROPERTY_NAMES)

            # If the primary guardian is not declared with an email address, we
            # replace them with the secondary guardian in this row, providing that
            # a secondary guardian has been declared.
            if cast.is_undefined(row[FamilyPropertyName.primary_guardian_email_address]):
                if cast.is_undefined(row[FamilyPropertyName.secondary_guardian_sis_id]):
                    raise ValueError(
                        f"The guardians of the child \"{row[FamilyPropertyName.child_sis_id]}\" "
                        "are not declared with an email address"
                    )

                logging.warning(
                    f"The primary guardian \"{row[FamilyPropertyName.primary_guardian_sis_id]} "
                    "is not declared with an email address; replacing them with the "
                    f"secondary guardian \"{row[FamilyPropertyName.secondary_guardian_sis_id]}\"..."
                )
                self._replace_primary_guardian_with_secondary_guardian(row)

        return rows

    @staticmethod
    def _clear_row_properties(
            row: dict[FamilyPropertyName, Any],
            fields: list[FamilyPropertyName]
    ) -> None:
        """
        Clear the value of the specified fields.


        :param row: The row of the family list where these fields need to be
            cleared.

        :param fields: The list of fields which value needs to be cleared.
        """
        for field in fields:
            row[field] = ''

    def _convert_field_boolean_value(self, value: str) -> bool:
        """
        Return the boolean value corresponding to the specified string
        representation.


        :note: We cannot make this function static because it must respect a
            common interface with other data conversion functions, some of
            which need access to protected/private members of this class.

        :param value: A string representation of a boolean.


        :return: A boolean.
        """
        return cast.string_to_boolean(value)

    def _convert_field_date_value(self, value: str) -> datetime.datetime:
        """
        Return the date value of a property of the family list data.


        :note: We cannot make this function static because it must respect a
            common interface with other data conversion functions, some of
            which need access to protected/private members of this class.


        :param value:


        :return: A date.


        :raise ValueError: If the string representation of the date doesn't
            comply with ISO 8601.
        """
        try:
            date = cast.string_to_date(value)
        except (ParserError, OverflowError) as error:
            logging.error(f"Invalid string representation \"{value}\" of a date")
            raise ValueError(str(error))

        return date

    def _convert_field_email_address_value(self, value: str | None) -> Contact | None:
        """
        Return the contact information representing the specified email
        address.


        :note: We cannot make this function static because it must respect a
            common interface with other data conversion functions, some of
            which need access to protected/private members of this class.

        :param value: A string representation of an email address.

        :return: A contact information.
        """
        return value and Contact(
            ContactName.EMAIL,
            value.lower(),
            is_primary=True,
            strict=True
        )

    def _convert_field_phone_number_value(self, value: str | None) -> Contact | None:
        """
        Return the contact information representing the specified phone number.


        :note: We cannot make this function static because it must respect a
            common interface with other data conversion functions, some of
            which need access to protected/private members of this class.

        :param value: A string representation of an international phone number.


        :return: A contact information.
        """
        if not value:
            return None

        # Remove any character from the value that is not a number or the sign
        # ``+``.
        cleanse_value = ''.join([
            c
            for c in value
            if c in string.digits or c == '+'
        ])

        return value and Contact(
            ContactName.PHONE,
            cleanse_value,
            is_primary=True,
            strict=True
        )

    @classmethod
    def _replace_primary_guardian_with_secondary_guardian(
            cls,
            row: dict[FamilyPropertyName, Any],
    ) -> None:
        """
        Replace the primary guardian with the secondary guardian.


        :note: This operation generally occurs when the primary guardian is
            not declared with a required identifier, such as an email address.


        :param row: The row of the family list where this replacement needs to
            be done.
        """
        for property_index in range(len(cls.PRIMARY_GUARDIAN_PROPERTY_NAMES)):
            primary_guardian_property_name = cls.PRIMARY_GUARDIAN_PROPERTY_NAMES[property_index]
            secondary_guardian_property_name = cls.SECONDARY_GUARDIAN_PROPERTY_NAMES[property_index]
            row[primary_guardian_property_name] = row[secondary_guardian_property_name]

        cls._clear_row_properties(row, cls.SECONDARY_GUARDIAN_PROPERTY_NAMES)

    @abc.abstractmethod
    def fetch_families_list(self) -> FamilyList:
        """
        Returns the data of the families to synchronize.


        :return: The data of the families to synchronize.
        """

    @property
    def vendor(self) -> SisVendor:
        return self.__vendor
