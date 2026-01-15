from NewsletterTools import NewsletterTools

# update standings
pipeline = NewsletterTools()
pipeline.get_standings()
pipeline.write_standings()

# update team snapshots
pipeline.write_team_snapshots()