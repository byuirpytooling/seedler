from seedler import *
import pandas as pd
import plotly.express as px

MAX_DRAWDOWN = 0

class MarketPlanter(Planter):
    def setup(self, initial_price, volatility, days):
        self.start = initial_price
        self.vol = volatility
        self.days = days
        return self

    def plant(self, sprout: Sprout):
        current_price = self.start
        lowest_price = self.start
        
        for _ in range(self.days):
            move = sprout.growth(-100, 100) / 1000.0 
            current_price *= (1 + (move * self.vol))
            
            if current_price < lowest_price:
                lowest_price = current_price
        
        drawdown = ((self.start - lowest_price) / self.start) * 100
        sprout.add_bud(MAX_DRAWDOWN, int(drawdown))

    def plant_verbose(self, sprout: Sprout):
        current_price = self.start
        
        for day in range(self.days):
            move = sprout.growth(-100, 100) / 1000.0 
            current_price *= (1 + (move * self.vol))
        
            change = (current_price / self.start) * 100
            sprout.add_bud(day, int(change))

class FindBlackSwan(Fire):
    def __init__(self, threshold=40):
        self.threshold = threshold

    def purge(self, sprout: Sprout):
        return sprout.get_bud_count(MAX_DRAWDOWN) < self.threshold

sims = 50_000

lab = MarketPlanter().setup(initial_price=100, volatility=0.15, days=356)
crashes = lab.find_seeds(fire=FindBlackSwan(40), maximum=sims)

crash_chance = len(crashes) / sims * 100

print(f"Crashes (down 40%, vol {lab.vol}): {crash_chance:>6.2f}% ({len(crashes)}/{sims})")


## GRAPHING CRASH YEAR MARKET
if len(crashes) == 0: quit

target_seeds = [c[0] for c in crashes[:200]]

all_paths = []

for seed_id in target_seeds:
    sprout = Sprout(seed_id)
    lab.plant_verbose(sprout)
    
    temp_df = pd.DataFrame(sprout.to_dict().items(), columns=['day', 'perc'])
    temp_df['seed'] = str(seed_id)  # Add seed ID as a label for Plotly
    all_paths.append(temp_df)

df_master = pd.concat(all_paths).sort_values(by=['seed', 'day']).reset_index(drop=True)

fig = px.line(
    df_master, 
    x="day", 
    y="perc", 
    line_group="seed",
    title=f"Top {len(target_seeds)} Black Swan Simulation Paths",
    template="plotly_white",
    render_mode="webgl"
)

fig.update_traces(
    line=dict(color="rgba(100, 110, 250, 0.2)", width=1),
    hoverlabel=dict(bgcolor="white"),
    hovertemplate="Seed: %{customdata[0]}<br>Day: %{x}<br>Percent: %{y}%<extra></extra>",
    customdata=df_master[['seed']]
)

fig.add_hline(
    y=60.0, 
    line_dash="dash", 
    line_color="red", 
    annotation_text="Crash Threshold",
    annotation_position="top left"
)

fig.update_layout(
    hovermode="closest",
    showlegend=False,
    yaxis_title="Percent of Starting Price",
    xaxis_title="Day of Simulation"
)

fig.show()