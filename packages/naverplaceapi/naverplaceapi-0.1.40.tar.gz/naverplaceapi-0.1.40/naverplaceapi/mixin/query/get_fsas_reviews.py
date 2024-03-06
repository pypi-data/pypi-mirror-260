def create(business_id: str, page_no: int, page_size: int):
    operation_name = 'getFsasReviews'
    variables = _define_variables(business_id, page_no, page_size)
    query = {
        "operationName": operation_name,
        "variables": variables,
        "query": QUERY_STATEMENT
    }
    return query


def _define_variables(business_id: str, page_no: int, page_size: int):
    return {
            "input":
                {
            "businessId": business_id,
            'businessType': 'restaurant',
            'deviceType': 'mobile',
            "display": page_size,
            "page": page_no
        }
    }


QUERY_STATEMENT = 'query getFsasReviews($input: FsasReviewsInput) {\n  fsasReviews(input: $input) {\n    ...FsasReviews\n    __typename\n  }\n}\n\nfragment FsasReviews on FsasReviewsResult {\n  total\n  maxItemCount\n  items {\n    name\n    type\n    typeName\n    url\n    home\n    id\n    title\n    rank\n    contents\n    bySmartEditor3\n    hasNaverReservation\n    thumbnailUrl\n    thumbnailUrlList\n    thumbnailCount\n    date\n    isOfficial\n    isRepresentative\n    profileImageUrl\n    isVideoThumbnail\n    reviewId\n    authorName\n    createdString\n    bypassToken\n    __typename\n  }\n  __typename\n}'
