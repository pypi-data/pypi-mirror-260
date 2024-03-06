"""
빌드 준비에 필요한 코드 호출
샘플입니다. 적절히 변경해서 사용해주세요.
"""


import api
import config
import traceback
import {{app}}.doc_maker
from {{app}}.model.sample_user import Address, User


def run():
    config.build = True
    # DB 초기화 등 진행.
    Address.sync_table()
    User.sync_table()
    api.locking.init_table()
    api.firehose_log.init()
    api.s3_public.init_s3_bucket()
    # 초기화 메서드를 제공하지 않는 리소스는, AWS Console 에서 직접 생성 요망

    if config.env == 'dev':
        {{app}}.doc_maker.make_api_doc()


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        raise Exception(f'Exception:{e}, \ntraceback:{traceback.format_exc()}')
        # 에러를 다시 발생시켜 CodeBuild가 실패 상태를 감지할 수 있도록 합니다.
