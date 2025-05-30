from dbt.tests.adapter.concurrency.test_concurrency import (
    BaseConcurrency,
    seeds__update_csv,
)
from dbt.tests.util import check_relations_equal, rm_file, run_dbt, write_file


class TestConcurrencyTrino(BaseConcurrency):
    def test_concurrency(self, project):
        run_dbt(["seed", "--select", "seed"])
        results = run_dbt(["run"], expect_pass=False)
        assert len(results) == 7
        check_relations_equal(project.adapter, ["SEED", "VIEW_MODEL"])
        check_relations_equal(project.adapter, ["SEED", "DEP"])
        check_relations_equal(project.adapter, ["SEED", "TABLE_A"])
        check_relations_equal(project.adapter, ["SEED", "TABLE_B"])

        rm_file(project.project_root, "seeds", "seed.csv")
        write_file(seeds__update_csv, project.project_root + "/seeds", "seed.csv")
        results = run_dbt(["run"], expect_pass=False)
        assert len(results) == 7
        check_relations_equal(project.adapter, ["SEED", "VIEW_MODEL"])
        check_relations_equal(project.adapter, ["SEED", "DEP"])
        check_relations_equal(project.adapter, ["SEED", "TABLE_A"])
        check_relations_equal(project.adapter, ["SEED", "TABLE_B"])
