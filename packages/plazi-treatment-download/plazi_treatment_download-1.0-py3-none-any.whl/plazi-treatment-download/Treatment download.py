import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os

# Fetch data from the given URL and parse XML to extract document IDs.
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        treatment_uuids = [doc.get('docId') for doc in root.findall('.//document')]
        return treatment_uuids
    else:
        return None

# Build a DataFrame with URLs and document IDs.
def build_dataframe(treatment_uuids, base_url):
    data_for_df = [{'URL': base_url + uuid, 'docId': uuid} for uuid in treatment_uuids]
    treatment_urls_df = pd.DataFrame(data_for_df)
    return treatment_urls_df

# Extract treatments and check for descriptions.
def extract_treatments(xml_content, treatment_urls_df):
    root = ET.fromstring(xml_content)
    data = []
    for result in root.findall('.//result'):
        document = result.find('.//document')
        if document is not None:
            doc_id = document.get('docId')
            treatment = document.find('.//treatment')
            if treatment is not None:
                gbif_taxon_id = treatment.get('ID-GBIF-Taxon')

                taxonomicName = treatment.find('.//taxonomicName')
                if taxonomicName is not None:
                    # Check for subSubSection with type="description"
                    description_exists = False
                    for subSubSection in treatment.findall('.//subSubSection'):
                        if subSubSection.get('type') == "description":
                            description_exists = True
                            break

                    taxon_data = {
                        'docId': doc_id,
                        'ID-GBIF-Taxon': gbif_taxon_id,
                        'class': taxonomicName.get('class'),
                        'family': taxonomicName.get('family'),
                        'genus': taxonomicName.get('genus'),
                        'kingdom': taxonomicName.get('kingdom'),
                        'phylum': taxonomicName.get('phylum'),
                        'species': taxonomicName.get('species'),
                        'Description Exists': description_exists
                    }
                    data.append(taxon_data)

    df = pd.DataFrame(data)
    combined_df = pd.merge(df, treatment_urls_df, on='docId', how='inner')
    return combined_df

# Download XML files for documents with descriptions.
def download_descriptions(combined_df, save_directory):
    for index, row in combined_df.iterrows():
        if row['Description Exists']:
            response = requests.get(row['URL'])
            if response.status_code == 200:
                filename = f"{row['docId']}.xml"
                filepath = os.path.join(save_directory, filename)
                with open(filepath, 'wb') as file:
                    file.write(response.content)

def main():
    url = "/path/to/save/directory/xml_download_only_description"
    # url = "https://tb.plazi.org/GgServer/search?fullText.ftQuery=bettles&resultPivot=100&resultFormat=XML"
    base_url = "https://tb.plazi.org/GgServer/xml/"

    save_directory = "/path/to/save/directory/xml_download_only_description"
    csv_file_path = "/path/to/save/directory/merge.csv"

    # save_directory = "/Users/panyaoru/Desktop/18-02-24_Plazi Pheno Trait/for code organization_V2.0/xml_download_only_description"
    # csv_file_path = "/Users/panyaoru/Desktop/18-02-24_Plazi Pheno Trait/for code organization_V2.0/merge.csv"

    treatment_uuids = fetch_data(url)
    if treatment_uuids is not None:
        treatment_urls_df = build_dataframe(treatment_uuids, base_url)
        combined_df = extract_treatments(requests.get(url).text, treatment_urls_df)
        combined_df.to_csv(csv_file_path, index=False)
        download_descriptions(combined_df, save_directory)
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    main()

main()
