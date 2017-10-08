def analyze_text(text):
    # Imports the Google Cloud client library
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types
    import six
    import argparse

    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    fullEntity = ""
    if len(entities) >= 1:
        fullEntity = entities[0].name
    if len(entities) < 1:
        fullEntity = "happy"

    for index, entity in enumerate(entities):
        if index != 0:
            fullEntity = fullEntity + " " + entity.name
    
    return fullEntity

def run_quickstart():
    print(analyze_text("I want to read a book!"))

if __name__ == '__main__':
    run_quickstart()