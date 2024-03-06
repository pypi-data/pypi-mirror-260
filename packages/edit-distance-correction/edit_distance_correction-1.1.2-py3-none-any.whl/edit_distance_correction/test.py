import time
import utils
from correction import Corrector

c = Corrector()
target_words = utils.read_files("target_words")
c.load_target_words(target_words)
test_words = utils.read_files("test_file", True)
start = time.time()
for w in test_words:
    print(w)
    res = c.recall_word(w)
    print(res)
    print(time.time() - start)
    start = time.time()
    print("\n")




#费时最大：stroke_res = [utils.max_backward_match(elem, self.target_word, max_k=10) for elem in cuts_stroke]
#形近字虽然用gram做了初筛，但不影响量级，相关组合太多n*n*n...

# c = Corrector()
# c.load_target_words(["1303XM2:1303XM26547891303XM2:1303XM281303XM2:1303XM2"])
# res = c.recall_word("16181")





