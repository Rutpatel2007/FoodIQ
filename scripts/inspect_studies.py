import sys
sys.path.insert(0, '.')
import backend.app.analytics.statistical_research as sr

print(f"RELATIONSHIP_STUDIES count: {len(sr.RELATIONSHIP_STUDIES)}")
for s in sr.RELATIONSHIP_STUDIES:
    print(f"  {s['study_id']}: {s['name']} ({s['company']} {s['segment']})")

results = sr.get_all_relationship_studies_with_fdr()
print(f"\nget_all_relationship_studies_with_fdr() returned: {len(results)} results")
for r in results:
    print(f"  {r['study_id']}: {r['name']} | N={r['sample_size']} | r={r.get('pearson_r')} | p={r.get('p_value')} | FDR={r.get('fdr_significant')}")

print(f"\nRESEARCH_WORKBENCH_QUESTIONS count: {len(sr.RESEARCH_WORKBENCH_QUESTIONS)}")
if isinstance(sr.RESEARCH_WORKBENCH_QUESTIONS, dict):
    for k, v in sr.RESEARCH_WORKBENCH_QUESTIONS.items():
        print(f"  {k}: {v['title']}")
else:
    for q in sr.RESEARCH_WORKBENCH_QUESTIONS:
        print(f"  {q['question_id']}: {q['title']}")
