from base import db
from base.com.vo.results_vo import ResultVO

class ResultsDAO:
    def insert_result(self, results_vo):
        db.session.add(results_vo)
        db.session.commit()
        
    def view_result(self):
        result_vo_list = ResultVO.query.all()  # returns list of ojects
        # print("VO:", category_vo_list, "\n\n\n")
        return result_vo_list
    
    # def view_result(self, results_vo):
    #     result_vo_list = ResultVO.query.get(results_vo.result_id) # returns list of ojects
    #     # print("VO:", category_vo_list, "\n\n\n")
    #     return result_vo_list