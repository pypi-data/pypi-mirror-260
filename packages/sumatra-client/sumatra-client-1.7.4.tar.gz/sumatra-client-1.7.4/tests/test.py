from sumatra import OptimizeClient
import time

c = OptimizeClient("console.sumatra.ai", workspace="noona")
opt_id = c.list_optimizations()[0]["id"]
exps = c.list_experiences(opt_id)
for exp in exps:
    if exp["status"] == "running":
        start = time.time()
        res = c.get_experiment_results(opt_id, exp["id"], exp["experimentId"], True)
        print(res)
        print(time.time() - start)
        print()
