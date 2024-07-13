import csv
from attrs import define, Factory
from pkrcomponents.components.utils.converters import pascal_to_snake_case

@define
class StreetHandStatsBase:

    def reset(self):
        """
        Resets the statistics
        """
        for attribute in self.__attrs_attrs__:
            # noinspection PyTypeChecker
            if isinstance(attribute.default, Factory):
                # noinspection PyUnresolvedReferences
                setattr(self, attribute.name, attribute.default.factory())
            else:
                setattr(self, attribute.name, attribute.default)

    @classmethod
    def generate_description_file(cls):
        """
        Generate a csv file to describe data from class
        """
        csv_file_name = f'{pascal_to_snake_case(cls.__name__)}_description.csv'
        with open(csv_file_name, 'w', newline='') as csvfile:
            fieldnames = ['name', 'default', 'description', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for attribute in cls.__attrs_attrs__:
                # noinspection PyTypeChecker
                row = {
                    'name': attribute.name,
                    'default': attribute.default if not isinstance(attribute.default, Factory)
                    else attribute.default.factory(),
                    'description': attribute.metadata.get('description', 'No description'),
                    'type': attribute.metadata.get('type', 'No type')
                }
                writer.writerow(row)
        print(f"CSV file '{csv_file_name}' generated successfully.")
