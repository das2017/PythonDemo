from flask import Blueprint, jsonify, request

from Spider.spiderDemo import Spider12306

queryModule = Blueprint('query', __name__)


@queryModule.route('/query/train', methods=['POST'])
def get_train():
    """
    这是火车票查询接口
    ---
    tags:
      - Query API
    parameters:
     - name: body
       in: body
       required: true
       schema:
           id: query
           properties:
             start:
               type: string
               description: 出发
               default: "上海虹桥"
             end:
               type: string
               description: 到达
               default: "深圳"
             date:
               type: string
               description: 出发时间
               default: "2019-06-06"
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: 机票查询数据
        schema:
          id: awesome
          properties:
            code:
              type: string
              description: The language name
              default: true
            data:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]
            message:
              type: string
              description: The language name
              default: ""
    """

    data = Spider12306().query_train(request.json["start"], request.json["end"], request.json["date"])
    if data['success']:
        return jsonify({"data": data['data'], "success": False, "message": "未查询到数据！"})
    return jsonify({"data": None, "success": False, "message": "未查询到数据！"})
