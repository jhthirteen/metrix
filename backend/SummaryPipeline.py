from NewsletterTools import NewsletterTools

summary_generator = NewsletterTools()
summary_generator.get_previous_day_games()
summary_generator.get_game_details()
summary_generator.rank_players_for_game()
summary_generator.generate_game_summary()
summary_generator.write_summaries()