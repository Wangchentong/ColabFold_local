import os
import argparse
import logging
from colabfold.batch import get_queries, run

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
 
    argparser.add_argument("--fasta_file", type=str, help="a3m file of predict sequence or contains msa")   
    argparser.add_argument('--num_cycles', default=3, type=int, help='the number of cycles to run alphafold')
    argparser.add_argument('--recycle_early_stop_tolerance', default=0.5, type=float, help='the number of cycles to run alphafold')
    argparser.add_argument('--models', nargs='+', default=[4],type=int, help='AlphaFold models to run (1-5)')
    argparser.add_argument('--num_seeds', type=int, default=1)
    argparser.add_argument('--model_type', type=str,default="alphafold2_multimer_v3",choices=["alphafold2_ptm","alphafold2_multimer_v3"])
    argparser.add_argument('--max_msa', type=str,default=None,choices=["512:1024", "256:512", "64:128", "32:64", "16:32"], help="max_msa:max_extra_msa for prediction diversity")
    
    args = argparser.parse_args()
    
    jobname = os.path.basename(args.fasta_file).split(".")[0]
    queries, is_complex = get_queries(args.fasta_file)
    print(f"job name : {queries[0][0]}" )
    print(f"query_sequence : {queries[0][1]}" )
    print(f"length of query_sequence : {len(queries[0][1])}")
    results = run(
        queries=queries,
        result_dir=jobname,
        use_templates=False,
        custom_template_path=None,
        num_relax=0,
        msa_mode="custom",
        model_type=args.model_type,
        num_models=len(args.models),
        num_recycles=args.num_cycles,
        relax_max_iterations=200,
        recycle_early_stop_tolerance=args.recycle_early_stop_tolerance,
        num_seeds=args.num_seeds,
        use_dropout=False,
        model_order=args.models,
        is_complex=is_complex,
        data_dir="/storage/caolongxingLab/wangchentong/software/ColabFold/alphafold/data/",
        keep_existing_results=False,
        rank_by="auto",
        max_msa=args.max_msa,
        use_cluster_profile=False if "multimer" in args.model_type and args.max_msa is not None else True,
        input_features_callback=None,
        save_recycles=False,
        user_agent=None,
    )