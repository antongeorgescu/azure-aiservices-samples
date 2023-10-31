import os
import azure.ai.vision as sdk

service_options = sdk.VisionServiceOptions("https://alvimager.cognitiveservices.azure.com/",
                                           "c484f033152443f28a7091ab0114fd6f")

_islocal = False
_localFiles =["presentation.png","flypage.png"]
_onlineFiles = ["https://www.corpnet.com/wp-content/uploads/2022/01/Legal-Document.jpg",
                "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1668782119i/40097951.jpg",
                "https://usedtotech.com/wp-content/uploads/2020/07/31-Easy-to-use-6-x-9-book-format-for-Word.jpg"]

if not _islocal:
    vision_source = sdk.VisionSource(url=_onlineFiles[2])
else:
    projectpath = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(projectpath, "images\\{}".format(_localFiles[1]))
    vision_source = sdk.VisionSource(filename=filepath)

analysis_options = sdk.ImageAnalysisOptions()

analysis_options.features = (
    sdk.ImageAnalysisFeature.CAPTION |
    sdk.ImageAnalysisFeature.TEXT
)

analysis_options.language = "en"

analysis_options.gender_neutral_caption = True

image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)

result = image_analyzer.analyze()

if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:

    if result.caption is not None:
        print(" Caption:")
        print("   '{}', Confidence {:.4f}".format(result.caption.content, result.caption.confidence))

    if result.text is not None:
        print(" Text & Words:")
        for line in result.text.lines:
            points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
            print("   Line: '{}', Bounding polygon {}".format(line.content, points_string))
            for word in line.words:
                points_string = "{" + ", ".join([str(int(point)) for point in word.bounding_polygon]) + "}"
                print("     Word: '{}', Bounding polygon {}, Confidence {:.4f}"
                      .format(word.content, points_string, word.confidence))
        print(" Text:")
        for line in result.text.lines:
            points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
            print("   Line: '{}'".format(line.content))
            

else:

    error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
    print(" Analysis failed.")
    print("   Error reason: {}".format(error_details.reason))
    print("   Error code: {}".format(error_details.error_code))
    print("   Error message: {}".format(error_details.message))