#!/usr/bin/env python
# File created on 21 Jul 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2011, Yoshiki Vazquez Baeza"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Release"

from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = "Trigger an OSX notification when a script"+\
    " of the QIIME family is executed"
script_info['script_description'] = "This command aims to integrate the "+\
    "family of QIIME python scripts with OSX's notification center by "+\
    "creating a notification everytime one of these programs finalizes it's "+\
    "execution."
script_info['script_usage'] = [("Process the last command that was executed",
    "Using a lookup list process the command that was las executed in the "
    "current bash session","%prog --command print_qiime_config.py")]
script_info['output_description']= "A notification will be presented in OSX's"+\
    " notification center."
script_info['required_options'] = [
    make_option('-c','--command',type="string",help='The command that we want '
    'to get a notification, only if it belongs to the QIIME family of scripts.')
]
script_info['optional_options'] = [
    make_option('-e','--exit_status',type="string",help='The command exit '
    'status.', default="0"),
    make_option('-s', '--make_sound', action="store_true", help='Whether or'
    ' not you want the notification to make a sound', default=False)
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    command_to_check = opts.command
    exit_status = opts.exit_status
    make_sound = opts.make_sound

    print command_to_check.split(' ')[0]

    if command_to_check.split(' ')[0] in AVAILABLE_COMMANDS:

        if exit_status == "0":
            text = "The command executed correctly"
        else:
            text = "There was a problem with the execution of the command (%s)"\
                % exit_status

        notify("Execution Finalized", "%s" % command_to_check, info_text=text,
            sound=make_sound)


def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={}):
    """ Python method to show a desktop notification on Mountain Lion. Where:
        title: Title of notification
        subtitle: Subtitle of notification
        info_text: Informative text of notification
        delay: Delay (in seconds) before showing the notification
        sound: Play the default notification sound
        userInfo: a dictionary that can be used to handle clicks in your
                  app's applicationDidFinishLaunching:aNotification method
    """
    from Foundation import NSDate
    from objc import lookUpClass

    NSUserNotification = lookUpClass('NSUserNotification')
    NSUserNotificationCenter = lookUpClass('NSUserNotificationCenter')

    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    notification.setUserInfo_(userInfo)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(NSDate.dateWithTimeInterval_sinceDate_(delay, NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

AVAILABLE_COMMANDS = [
# QIIME
'add_alpha_to_mapping_file.py',
'add_qiime_labels.py',
'add_taxa.py',
'adjust_seq_orientation.py',
'align_seqs.py',
'alpha_diversity.py',
'alpha_rarefaction.py',
'ampliconnoise.py',
'assign_taxonomy.py',
'beta_diversity.py',
'beta_diversity_through_plots.py',
'beta_significance.py',
'blast_wrapper.py',
'categorized_dist_scatterplot.py',
'check_id_map.py',
'clean_raxml_parsimony_tree.py',
'cluster_quality.py',
'collate_alpha.py',
'compare_3d_plots.py',
'compare_alpha_diversity.py',
'compare_categories.py',
'compare_distance_matrices.py',
'compare_taxa_summaries.py',
'compute_core_microbiome.py',
'conditional_uncovered_probability.py',
'consensus_tree.py',
'convert_fastaqual_fastq.py',
'convert_otu_table_to_unifrac_sample_mapping.py',
'convert_unifrac_sample_mapping_to_otu_table.py',
'core_diversity_analyses.py',
'core_qiime_analyses.py',
'count_seqs.py',
'demultiplex_fasta.py',
'denoise_wrapper.py',
'denoiser.py',
'denoiser_preprocess.py',
'denoiser_worker.py',
'detrend.py',
'dissimilarity_mtx_stats.py',
'distance_matrix_from_mapping.py',
'exclude_seqs_by_blast.py',
'extract_seqs_by_sample_id.py',
'filter_alignment.py',
'filter_distance_matrix.py',
'filter_fasta.py',
'filter_otus_by_sample.py',
'filter_otus_from_otu_table.py',
'filter_samples_from_otu_table.py',
'filter_taxa_from_otu_table.py',
'filter_tree.py',
'fix_arb_fasta.py',
'identify_chimeric_seqs.py',
'identify_missing_files.py',
'inflate_denoiser_output.py',
'insert_seqs_into_tree.py',
'jackknifed_beta_diversity.py',
'load_remote_mapping_file.py',
'make_2d_plots.py',
'make_3d_plots.py',
'make_bipartite_network.py',
'make_bootstrapped_tree.py',
'make_distance_boxplots.py',
'make_distance_comparison_plots.py',
'make_distance_histograms.py',
'make_fastq.py',
'make_library_id_lists.py',
'make_otu_heatmap.py',
'make_otu_heatmap_html.py',
'make_otu_network.py',
'make_otu_table.py',
'make_per_library_sff.py',
'make_phylogeny.py',
'make_prefs_file.py',
'make_qiime_py_file.py',
'make_qiime_rst_file.py',
'make_rarefaction_plots.py',
'make_tep.py',
'map_reads_to_reference.py',
'merge_mapping_files.py',
'merge_otu_maps.py',
'merge_otu_tables.py',
'multiple_rarefactions.py',
'multiple_rarefactions_even_depth.py',
'neighbor_joining.py',
'nmds.py',
'otu_category_significance.py',
'parallel_align_seqs_pynast.py',
'parallel_alpha_diversity.py',
'parallel_assign_taxonomy_blast.py',
'parallel_assign_taxonomy_rdp.py',
'parallel_beta_diversity.py',
'parallel_blast.py',
'parallel_identify_chimeric_seqs.py',
'parallel_map_reads_to_reference.py',
'parallel_multiple_rarefactions.py',
'parallel_pick_otus_blast.py',
'parallel_pick_otus_trie.py',
'parallel_pick_otus_uclust_ref.py',
'parallel_pick_otus_usearch61_ref.py',
'per_library_stats.py',
'pick_closed_reference_otus.py',
'pick_de_novo_otus.py',
'pick_open_reference_otus.py',
'pick_otus.py',
'pick_otus_through_otu_table.py',
'pick_reference_otus_through_otu_table.py',
'pick_rep_set.py',
'pick_subsampled_reference_otus_through_otu_table.py',
'plot_rank_abundance_graph.py',
'plot_semivariogram.py',
'plot_taxa_summary.py',
'poller.py',
'poller_example.py',
'principal_coordinates.py',
'print_metadata_stats.py',
'print_qiime_config.py',
'process_iseq.py',
'process_qseq.py',
'process_sff.py',
'quality_scores_plot.py',
'relatedness.py',
'shared_phylotypes.py',
'simsam.py',
'single_rarefaction.py',
'sort_otu_table.py',
'split_fasta_on_sample_ids.py',
'split_libraries.py',
'split_libraries_fastq.py',
'split_otu_table.py',
'split_otu_table_by_taxonomy.py',
'start_parallel_jobs.py',
'start_parallel_jobs_sc.py',
'start_parallel_jobs_torque.py',
'submit_to_mgrast.py',
'subsample_fasta.py',
'summarize_otu_by_cat.py',
'summarize_taxa.py',
'summarize_taxa_through_plots.py',
'supervised_learning.py',
'transform_coordinate_matrices.py',
'tree_compare.py',
'trflp_file_to_otu_table.py',
'trim_sff_primers.py',
'truncate_fasta_qual_files.py',
'truncate_reverse_primer.py',
'unweight_fasta.py',
'upgma_cluster.py',
'validate_demultiplexed_fasta.py',
# EMPEROR
'make_emperor.py']

if __name__ == "__main__":
    main()

