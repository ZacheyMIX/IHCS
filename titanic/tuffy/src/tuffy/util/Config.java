package tuffy.util;

import java.io.BufferedWriter;
import java.io.PrintWriter;
import java.lang.management.ManagementFactory;
import java.util.HashSet;


/**
 * Container for global configuration parameters.
 */
public class Config {

	public static PrintWriter sampleLog = null;
	public static String samplerWriterPath = null;
	
	public static String product_line = "tuffy";
	public static String product_name = "Tuffy 0.3";
	public static String path_conf = "./tuffy.conf";

	public static boolean snapshot_mode = false;
	public static boolean snapshoting_so_do_not_do_init_flip = false;
	public static int currentSampledNumber = 0;

	public static boolean no_pushdown = false;
	
	public static boolean using_greenplum = false;

	public static boolean skipUselessComponents = true;
	
	public static boolean mark_atoms_in_useful_components = false;

	public static boolean activate_soft_evid = true;
	
	public static boolean count_only_useful_inconsistencies = false;

	public static boolean warmTuffy = false;
	

	public static boolean log_trace = true;
	
	/**
	 * Runtime
	 */
	public static boolean exiting_mode = false;
	public static boolean learning_mode = false;

	public static String display_marker;

	/**
	 * DB
	 */
	public static String relConstants = "constants";

	public static String db_url = "jdbc:postgresql://localhost:5432/postgres";
	public static String db_username = "tuffer";

	public static String db_password = "czhang";
	public static String db_schema = "a";

	public static boolean constants_as_raw_string = false;

	/**
	 * File System
	 */
	public static String dir_working = "/tmp/tuffy-workspace";
	public static String dir_out = ".";
	public static boolean output_files_in_gzip = false;
	public static String dir_tests = "/tmp/tuffy-tests";
	public static String file_stats = "tuffy_stats.txt";

	/**
	 * System
	 */
	public static boolean disable_partition = false;
	public static int max_threads = 0;
	public static boolean build_predicate_table_indexes = false;
	public static int evidence_file_chunk_size = 1 << 22;
	public static double partition_size_bound = 1L << 32;
	public static double ram_size = 1L << 32;
	
	public static int max_number_components_per_bucket = Integer.MAX_VALUE;

	public static String evidDBSchema = null;
	public static boolean dbNeedTranslate = false;

	public static boolean reuseTables = false;

	public static boolean sortWhenParitioning = false;

	/*
	private static String[] aGoodTables = {"pred_mentionfeature_textngram1",
		"pred_mentionfeature_textalphanumeric_lc","pred_mentionfeature_textnumwords",
		"pred_mentionfeature_textalphanumeric","type_eid","type_docid","type_sentid",
		"pred_mentionfeature_textabbreviation","type_mid","pred_mentionfeature_type",
		"pred_mentionfeature_textlc","type_word","pred_fullmention"};
	private static String[] aVolatileTables = {"pred_query", "pred_mcoref_scope", 
		"pred_mcoref_map", "pred_asqueryfull"}; 
	public static HashSet<String> goodTables = new HashSet<String>();
	public static HashSet<String> volatileTables = new HashSet<String>();
	static {
		for (String t : aGoodTables) {
			goodTables.add(t);
		}
		goodTables.clear();
		for (String t : aVolatileTables) {
			volatileTables.add(t);
		}
		
	}
	*/



	/**
	 * Inference
	 */
	public static boolean use_atom_blocking = false;
	public static boolean mark_all_atoms_active = false;
	public static boolean stop_samplesat_upon_sat = false;

	public static double soft_evidence_activation_threshold = 0;
	public static double samplesat_sa_coef = 10;
	public static double mcsat_sample_para = 1;
	public static double hard_weight = 5.2E7;
	public static double hard_threshold = 1E7;
	public static double walksat_random_step_probability = 0.5;
	public static double sweepsat_greedy_probability = 0.5;
	public static boolean avoid_breaking_hard_clauses = false;
	public static boolean apply_greedy_throttling = true;

	public static boolean ground_atoms_ignore_neg_embedded_wgts = false;
	
	public static enum TUFFY_INFERENCE_TASK {MAP, MARGINAL, MLE};

	public static int gauss_seidel_infer_rounds = 5;
	
	public static boolean key_constraint_allows_null_label = false;

	/**
	 * UI
	 */
	public static int verbose_level = 0;
	public static String console_line_header = null;
	public static boolean clause_display_multiline = true;

	public static enum MCSAT_OUTPUT_TUPLE_ORDER {PROBABILITY, PRED_ARGS};
	public static MCSAT_OUTPUT_TUPLE_ORDER mcsat_output_order =
			MCSAT_OUTPUT_TUPLE_ORDER.PROBABILITY;

	public static double marginal_output_min_prob = 0;
	public static boolean mcsat_output_hidden_atoms = false;
	public static int mcsat_dump_interval = 0;
	
	public static boolean mcsat_cumulative = false;

	public static boolean enron_exp = true;
	public static boolean silent_on_single_thread = true;
	
	/**
	 * Helper
	 */
	public static int mcsatDumpPeriodSamples = 20;
	public static int mcsatDumpPeriodSeconds = 0;

	public static boolean output_prolog_format = false;
	public static boolean output_prior_with_marginals = true;
	public static boolean throw_exception_when_dying = false;

	public static boolean keep_db_data = false;

	public static boolean track_clause_provenance = false;
	public static boolean reorder_literals = false;

	public static double timeout = Double.MAX_VALUE;
	public static int num_tries_per_periodic_flush = 0;


	/**
	 * Research
	 */
	public static boolean checkNumCriticalNodes = false;
	public static boolean focus_on_critical_atoms = false;

	
	//public static int mleTopK = 100;
	public static int mleTopK = -1;
	// very expensive
	public static boolean calcRealMLECost = false;
	public static int innerPara = 1;
	public static int nMLESamples = 10000;
	
	public static boolean addReporter = true;	
	public static boolean debug_mode = false;
	
	public static int mle_gibbs_mcmc_steps = 10;
	public static boolean mle_use_key_constraint = true;
	
	public static boolean mle_optimize_small_components = false;
	public static boolean mle_partition_components = false;
	
	public static boolean mle_use_gibbs_sampling = false;
	public static boolean mle_use_mcsat_sampling = false;
	public static boolean mle_use_serialmix_sampling = false;
	public static boolean mle_use_junction_tree = false;
	
	public static int mle_serialmix_constant = 100;
	
	public static int getNumThreads(){
		if(max_threads > 0) return max_threads;
		return Runtime.getRuntime().availableProcessors();
	}


	public static String getLoadingDir(){
		String path = dir_working + "/loading";
		FileMan.ensureExistence(path);
		return path;
	}

	public static String getWorkingDir(){
		return dir_working;
	}

	public static int globalCounter = 0;

	public static int getNextGlobalCounter(){
		synchronized(Config.class) {
			globalCounter = globalCounter + 1;
			return globalCounter;
		}
	}
	
	

	public static String getProcessID(){
		return ManagementFactory.getRuntimeMXBean().getName();
	}
	
	public static double logAdd(double logX, double logY) {

	       if (logY > logX) {
	           double temp = logX;
	           logX = logY;
	           logY = temp;
	       }

	       if (logX == Double.NEGATIVE_INFINITY) {
	           return logX;
	       }
	       
	       double negDiff = logY - logX;
	       if (negDiff < -200) {
	           return logX;
	       }
	       
	       return logX + java.lang.Math.log(1.0 + java.lang.Math.exp(negDiff)); 
	 }

}
