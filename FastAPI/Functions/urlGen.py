from Functions.uploadFileToS3 import upload_file_to_s3


# function to generate file download link from filename

def geos_url_gen(filename):
    # slice filename to exctract path parameters
    arr = filename.split("_")
    tproduct_code = arr[1].split("-")
    s1 = tproduct_code[2]
    station = tproduct_code[0] + "-" + tproduct_code[1] + "-" + ''.join([i for i in s1 if not i.isdigit()])
    date = arr[3]
    year = date[1:5]
    day = date[5:8]
    hour = date[8:10]
    # define path
    path = "{}/{}/{}/{}/".format(station, year, day, hour)
    # Function returns download link
    url = upload_file_to_s3(filename, path, "noaa-goes18", "the-data-guys")
    return {"link": url}


def nexrad_url_gen(filename):
    # slice filename to exctract path parameters
    station = filename[:4]
    year = filename[4:8]
    month = filename[8:10]
    day = filename[10:12]
    # define path
    path = "{}/{}/{}/{}/".format(year, month, day, station)
    # Function returns download link
    url = upload_file_to_s3(filename, path, "noaa-nexrad-level2", "the-data-guys")
    return {"link": url}
