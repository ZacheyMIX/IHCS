from View import View
# from ViewModel import ViewModel
# from backend import data_formatting_pipeline, data_evaluation_pipeline
# from backend.mln_files.pipeline import run_mln_pipeline

if __name__ == "__main__":
    View.begin()

#MLN Rule Format Guide

#Start with all the predicates you want to use

# Write logic rules using this format:

# 0.9 HasEmail(e, email), RegexMatch(email, " ") => BadEmail(e)

# Use RegexMatch(field, pattern) for pattern checks

# Use Bad<Field> or Weird<Field> to flag errors

# Weight is optional but recommended (range: 0.0 to 1.0)