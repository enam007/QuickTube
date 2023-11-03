import utils
def getVideoInfo(url):
    video_type = utils.identify_video_service(url)
    video_id = utils.extract_video_id(url,video_type)
    if video_type == "YouTube":
        return utils.get_video_info(url,video_id)
    elif video_type == "Vimeo":
        return utils.get_vimeo_video_info(video_id)