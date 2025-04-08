# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime
# import seaborn as sns
# from pathlib import Path
# import numpy as np

# class ReportGenerator:
#     def __init__(self, output_dir="reports"):
#         self.output_dir = Path(output_dir)
#         self.output_dir.mkdir(exist_ok=True)
        
#     def generate_report(self, analysis_results):
#         """Generate a comprehensive analysis report"""
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         report_path = self.output_dir / f"analysis_report_{timestamp}"
        
#         # Create report directory
#         report_path.mkdir(exist_ok=True)
        
#         # Generate visualizations
#         self._create_score_radar(analysis_results, report_path)
#         self._create_vocabulary_analysis(analysis_results, report_path)
        
#         # Generate detailed report
#         self._generate_text_report(analysis_results, report_path)
        
#         return report_path
    
#     def _create_score_radar(self, results, report_path):
#         """Create radar chart of various scores"""
#         categories = ['Pronunciation', 'Grammar', 'Vocabulary', 'Fluency']
#         scores = [
#             results.get('pronunciation_score', 0),
#             results.get('grammar_score', 0),
#             results.get('vocabulary_score', 0),
#             results.get('fluency_score', 0)
#         ]
        
#         # Create radar chart
#         angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
#         scores = np.concatenate((scores, [scores[0]]))
#         angles = np.concatenate((angles, [angles[0]]))
        
#         fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
#         ax.plot(angles, scores)
#         ax.fill(angles, scores, alpha=0.25)
#         ax.set_xticks(angles[:-1])
#         ax.set_xticklabels(categories)
        
#         plt.savefig(report_path / 'radar_chart.png')
#         plt.close()
    
#     def _create_vocabulary_analysis(self, results, report_path):
#         """Create vocabulary analysis visualizations"""
#         vocab_data = results.get('vocabulary_analysis', {})
        
#         # Create bar chart for vocabulary metrics
#         plt.figure(figsize=(10, 6))
#         metrics = ['lexical_diversity', 'sophistication', 'context_appropriateness']
#         values = [vocab_data.get(metric, 0) for metric in metrics]
        
#         sns.barplot(x=metrics, y=values)
#         plt.title('Vocabulary Analysis Metrics')
#         plt.xticks(rotation=45)
        
#         plt.savefig(report_path / 'vocabulary_analysis.png', bbox_inches='tight')
#         plt.close()
    
#     def _generate_text_report(self, results, report_path):
#         """Generate detailed text report"""
#         report_content = [
#             "Communication Assessment Report",
#             "=" * 30,
#             f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
#             "\nOverall Scores:",
#             f"- Pronunciation: {results.get('pronunciation_score', 0):.2f}",
#             f"- Grammar: {results.get('grammar_score', 0):.2f}",
#             f"- Vocabulary: {results.get('vocabulary_score', 0):.2f}",
#             f"- Fluency: {results.get('fluency_score', 0):.2f}",
#             "\nDetailed Analysis:",
#             "1. Grammar Corrections:",
#             results.get('grammar_feedback', 'No feedback available'),
#             "\n2. Vocabulary Usage:",
#             f"- Unique words: {results.get('vocabulary_analysis', {}).get('unique_words', 0)}",
#             f"- Lexical diversity: {results.get('vocabulary_analysis', {}).get('lexical_diversity', 0):.2f}",
#             "\n3. Pronunciation Details:",
#             f"- Confidence score: {results.get('pronunciation_analysis', {}).get('confidence_scores', 0):.2f}",
#             f"- Stress pattern score: {results.get('pronunciation_analysis', {}).get('stress_patterns', 0):.2f}"
#         ]
        
#         with open(report_path / 'detailed_report.txt', 'w') as f:
#             f.write('\n'.join(report_content)) 