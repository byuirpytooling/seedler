from seedler import *
import pandas as pd
import plotly.express as px

FAILURE_POINT = 1

class BridgePlanter(Planter):
    def setup(self, damping_factor, gust_sensitivity, duration):
        self.damping = damping_factor
        self.sensitivity = gust_sensitivity
        self.duration = duration
        return self

    def plant(self, sprout: Sprout):
        oscillation = 0.0
        max_oscillation = 0.0
        
        for _ in range(self.duration):
            # Simulate random wind gust
            gust = sprout.growth(-100, 100) / 100.0
            force = gust * self.sensitivity
            
            # Update physical state with damping
            oscillation = (oscillation + force) * self.damping
            
            if abs(oscillation) > max_oscillation:
                max_oscillation = abs(oscillation)
        
        sprout.add_bud(FAILURE_POINT, int(max_oscillation))

    def plant_verbose(self, sprout: Sprout):
        oscillation = 0.0
        
        for step in range(self.duration):
            gust = sprout.growth(-100, 100) / 100.0
            force = gust * self.sensitivity
            oscillation = (oscillation + force) * self.damping
            
            sprout.add_bud(step, abs(int(oscillation)))

class FindCollapse(Fire):
    def __init__(self, threshold=1000):
        self.threshold = threshold

    def purge(self, sprout: Sprout):
        # Discard seeds that stay below the collapse threshold
        return sprout.get_bud_count(FAILURE_POINT) < self.threshold
    

sims = 1_000_000

lab = BridgePlanter().setup(damping_factor=0.99, gust_sensitivity=50.0, duration=500)
failures = lab.find_seeds(fire=FindCollapse(1000), maximum=sims)

failure_rate = len(failures) / sims * 100

print(f"Collapses (threshold 1000): {failure_rate:>6.3f}% ({len(failures)}/{sims})")

if len(failures) == 0: quit()

target_seeds = [f[0] for f in failures[:5]]
all_paths = []

for seed_id in target_seeds:
    sprout = Sprout(seed_id)
    lab.plant_verbose(sprout)
    
    temp_df = pd.DataFrame(sprout.to_dict().items(), columns=['step', 'amplitude'])
    temp_df['seed'] = str(seed_id)
    all_paths.append(temp_df)

df_master = pd.concat(all_paths).sort_values(by=['seed', 'step']).reset_index(drop=True)

fig = px.line(
df_master,
x="step",
y="amplitude",
color="seed",
title=f"Resonance Failure Paths (n={len(target_seeds)})",
template="plotly_white",
render_mode="webgl"
)

fig.add_hline(
    y=1000.0, 
    line_dash="dash", 
    line_color="black", 
    annotation_text="Structural Limit"
)

fig.update_layout(
    hovermode="closest",
    showlegend=False,
    yaxis_title="Oscillation Amplitude (ABS)",
    xaxis_title="Time Step"
)

fig.show()