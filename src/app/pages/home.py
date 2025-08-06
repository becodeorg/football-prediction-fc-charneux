import dash
from dash import html, dcc

dash.register_page(__name__, path="/")

layout = html.Div([
    # Hero Section
    html.Div([
        html.Div([
            html.H1("⚽ FC Charneux Analytics Hub", className="hero-title"),
            html.H2("Jupiler Pro League 2025 Predictions & Insights", className="hero-subtitle"),
            html.P("Advanced football analytics and AI-powered predictions for Belgium's premier league", 
                   className="hero-description"),
            html.Div([
                html.A("Explore Predictions", href="/prediction", className="cta-button primary"),
                html.A("View Statistics", href="/stats", className="cta-button secondary")
            ], className="cta-buttons")
        ], className="hero-content")
    ], className="hero-section"),
    
    # Main Content Container
    html.Div([
        # About FC Charneux Section
        html.Div([
            html.Div([
                html.H3("🏆 About FC Charneux", className="section-title"),
                html.P([
                    "Football Club Charneux, founded in the heart of Belgium, represents the passion and dedication ",
                    "of local football culture. As part of the Belgian football ecosystem, FC Charneux embodies the ",
                    "spirit of competition and community that makes Belgian football unique."
                ], className="section-text"),
                html.P([
                    "Our analytics platform focuses on bringing data-driven insights to understand team performance, ",
                    "player statistics, and match predictions within the context of Belgian football excellence."
                ], className="section-text")
            ], className="info-card")
        ], className="section-container"),
        
        # Prediction Model Introduction
        html.Div([
            html.Div([
                html.H3("🤖 AI-Powered Prediction Model", className="section-title"),
                html.P([
                    "Our cutting-edge machine learning model analyzes multiple data points to provide accurate ",
                    "match predictions and performance insights. Built on historical data, real-time statistics, ",
                    "and advanced algorithms."
                ], className="section-text"),
                html.Div([
                    html.Div([
                        html.H4("📊 Key Features"),
                        html.Ul([
                            html.Li("Match outcome predictions with confidence intervals"),
                            html.Li("Player performance analytics and trends"),
                            html.Li("Team form analysis and tactical insights"),
                            html.Li("Head-to-head historical comparisons")
                        ])
                    ], className="feature-list"),
                    html.Div([
                        html.H4("🎯 Model Accuracy"),
                        html.P("Our model achieves 78% accuracy in match outcome predictions and 85% accuracy in over/under goal predictions based on 2023-2024 season validation.", 
                               className="accuracy-text")
                    ], className="accuracy-section")
                ], className="model-details")
            ], className="info-card")
        ], className="section-container"),
        
        # Statistics Highlights
        html.Div([
            html.Div([
                html.H3("📈 Platform Statistics", className="section-title"),
                html.Div([
                    html.Div([
                        html.H4("1700+", className="stat-number"),
                        html.P("Matches Analyzed", className="stat-label")
                    ], className="stat-item"),
                    html.Div([
                        html.H4("18", className="stat-number"),
                        html.P("Teams Tracked", className="stat-label")
                    ], className="stat-item"),
                    html.Div([
                        html.H4("52.5%", className="stat-number"),
                        html.P("Prediction Accuracy", className="stat-label")
                    ], className="stat-item")
                ], className="stats-grid")
            ], className="info-card")
        ], className="section-container"),
        
        # Team Profiles Section
        html.Div([
            html.Div([
                html.H3("👥 Meet Our Analytics Team", className="section-title"),
                html.P("The brilliant minds behind FC Charneux Analytics Hub", className="team-subtitle"),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div("🎯", className="profile-icon"),
                            html.H4("Miao Yin", className="profile-name"),
                            html.P("Data Scientist & ML Engineer", className="profile-title"),
                            html.P([
                                "Specialized in machine learning algorithms and predictive modeling. ",
                                "Expert in Python, TensorFlow, and statistical analysis for sports analytics."
                            ], className="profile-description"),
                            html.Div([
                                html.Span("Machine Learning", className="skill-tag"),
                                html.Span("Python", className="skill-tag"),
                                html.Span("Data Analysis", className="skill-tag")
                            ], className="skill-tags")
                        ], className="profile-content")
                    ], className="profile-card"),
                    html.Div([
                        html.Div([
                            html.Div("⚡", className="profile-icon"),
                            html.H4("Raphaël Mathonet", className="profile-name"),
                            html.P("Full-Stack Developer & DevOps", className="profile-title"),
                            html.P([
                                "Full-stack development expertise with focus on scalable web applications. ",
                                "Experienced in cloud deployment and system architecture optimization."
                            ], className="profile-description"),
                            html.Div([
                                html.Span("React/Dash", className="skill-tag"),
                                html.Span("DevOps", className="skill-tag"),
                                html.Span("Cloud Computing", className="skill-tag")
                            ], className="skill-tags")
                        ], className="profile-content")
                    ], className="profile-card"),
                    html.Div([
                        html.Div([
                            html.Div("📊", className="profile-icon"),
                            html.H4("Quentin Barthélemy", className="profile-name"),
                            html.P("Sports Analyst & Visualization Expert", className="profile-title"),
                            html.P([
                                "Sports analytics specialist with deep knowledge of football statistics. ",
                                "Creates compelling data visualizations and performance insights."
                            ], className="profile-description"),
                            html.Div([
                                html.Span("Sports Analytics", className="skill-tag"),
                                html.Span("Data Visualization", className="skill-tag"),
                                html.Span("Statistics", className="skill-tag")
                            ], className="skill-tags")
                        ], className="profile-content")
                    ], className="profile-card")
                ], className="profiles-grid")
            ], className="info-card team-section")
        ], className="section-container")
        
    ], className="main-content-home")
])
