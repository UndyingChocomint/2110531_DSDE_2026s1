# CCTV Application: Bangkok Traffic Pulse

End-to-end data science project built on the Bangkok CCTV image dataset (100 cameras, about 61k images, 604-631 images per camera).

**Persona:** a marketing person who wants transport-related insights for customers, using CCTV pictures as the data source.
**Goal:** a project that keeps being useful after it is built, not a one-off analysis.

---

## 1. Instructions (from the `Task` file)

- Team of up to 3 members.
- Show an end-to-end data science workflow with a practical application or meaningful insight.
- Four required components:

| # | Component | Requirement |
|---|-----------|-------------|
| 1 | Data engineering | Cleansing, preparation, and ideally workflow management so the whole process runs end to end. Web scraping does not count. |
| 2 | Data science | Analytical methods that explore patterns, trends and insights in the prepared data. |
| 3 | BI dashboard | Dashboard on the transportation data. |
| 4 | Insights | The outcome of the analysis. |

- Extra points for: workflow quality, additional components, deeper analysis.

## 2. Input files

| File | What it is |
|------|------------|
| `dataset` | Description and Google Drive link to the CCTV images |
| `Task` | Project instructions (above) |
| `cctv_info.csv` | 100 cameras: id, Thai/English location, latitude, longitude, ip_address, image_count |
| `png2pdf.pdf` | Flowchart: CCTV picture, what can we see, three personas |
| `png2pdf-1.pdf` | Objective document (could not be read yet, see Blockers) |

## 3. Idea (from the flowchart)

CCTV pictures give: camera timestamp, vehicle type, camera ID. Three personas use them:

1. **Rider (Uber-style):** where does a car arrive fastest, shortest distance.
2. **Transport administrator:** where is traffic heavy, what needs maintenance, control policy.
3. **Carbon project:** estimated emissions by vehicle type and area.

### Candidate analyses (pick a core set)

1. Weather and visibility vs. traffic (rain, glare, night)
2. Camera clustering by hourly pattern and vehicle mix
3. Peak-hour baseline and anomaly detection
4. Short-term traffic forecast
5. Pipeline quality monitor (missing or dark frames, detector accuracy by lighting, dead cameras)
6. Carbon proxy by area

**Suggested package:** 1, 2 and 5 as the core; 3 or 4 as the extra.

## 4. Planned pipeline

```
Drive images -> ingest -> validate (missing/blurry/dark) -> vehicle detection
  -> clean table (camera_id, timestamp, vehicle_type, count, condition)
  -> analysis (stats, clustering, time series) -> BI dashboard -> insights
```

Scheduled with a workflow tool (for example Airflow or Prefect). Store counts, not images, so history is cheap to keep and privacy risk stays low.

## 5. Task to do

### Setup
- [ ] Get access to the images (download or mount the Drive folder).
- [ ] Inspect sample images: is there a usable timestamp (filename or overlay)?
- [ ] Read `png2pdf-1.pdf` and confirm the Objective matches this README.
- [ ] Decide team split (max 3): pipeline, analysis, dashboard.

### Component 1: Data engineering
- [ ] Ingest script that lists and loads images per camera.
- [ ] Parse timestamp and camera ID per image.
- [ ] Data quality checks (missing, duplicate, blurry, dark frames).
- [ ] Vehicle detection (car, motorcycle, bus, truck) and write the clean table.
- [ ] Join with `cctv_info.csv` (location, coordinates).
- [ ] Workflow scheduler running the steps end to end.

### Component 2: Data science
- [ ] EDA: counts by hour, camera, vehicle type.
- [ ] Chosen analyses from section 3 (core plus extra).
- [ ] Validate detector accuracy on a hand-labelled sample, split by lighting.

### Component 3: BI dashboard
- [ ] Replace simulated numbers in the prototype with the real table.
- [ ] Views for the three personas, plus a data-quality view.
- [ ] Add a street basemap if the final host allows it.

### Component 4: Insights
- [ ] Write findings and recommendations per persona.
- [ ] Agree and document metric definitions (for example what "busy" means).
- [ ] Get a second review (another agent or teammate) against the Task and flowchart.

### Bonus (extra points)
- [ ] Model monitoring and retraining plan.
- [ ] Forecast or anomaly alerts.

## 6. Current progress

| Item | Status |
|------|--------|
| Read Task, dataset note, flowchart | Done |
| Profile `cctv_info.csv` (100 unique cameras, 604-631 images each, 4 cameras with placeholder English names) | Done |
| Brainstorm campaign ideas | Done |
| Long-life project direction ("Traffic Pulse") | Done |
| Requirements and new-ideas doc | Done: https://claude.ai/artifact/N6NXJ8E29aVK3XoDKwvAgJ |
| Prototype dashboard (3 persona views) | Done, but vehicle counts, congestion and CO2 are **simulated**: https://claude.ai/artifact/AX1kRSMqNBVgALU6nRAwMz |
| Image access and vehicle detection | Not started |
| Cleaning pipeline and scheduler | Not started |
| Real analysis and insights | Not started |
| Second-agent review | Not done (a self-review was written; a real second review is still needed) |

### Real vs. simulated in the prototype
- Real: camera locations, names, coordinates, image counts.
- Simulated: all vehicle counts, congestion, vehicle mix, CO2.

## 7. Blockers and risks

1. The Drive images were not reachable from the build environment, so no image has been inspected.
2. `png2pdf-1.pdf` is listed in the project but could not be opened.
3. Timestamps in the images are unverified. Analyses 3 and 4 depend on them.
4. Long-term use needs a legitimate way to keep re-fetching new images; otherwise the project stays a snapshot.

## 8. Next step

Upload sample images (or one camera's filenames) so the timestamp question can be answered, then build the ingest and detection step.

## 9. Generated Ideas

| # | Name | Interest | Feasibility | Novelty | Score |
|---|------|:--------:|:-----------:|:-------:|:-----:|
| 1 | camera_archetype_clustering | 7 | 8 | 5 | 6 |
| 2 | visibility_count_correlation | 8 | 7 | 7 | 7 |
| 3 | co2_proxy_heatmap | 8 | 6 | 6 | 6 |
| 4 | rolling_baseline_anomaly | 7 | 7 | 5 | 6 |
| 5 | cross_camera_travel_time | 9 | 5 | 8 | 7 |

**Titles:**

1. **camera_archetype_clustering** — Discovering Bangkok Traffic Archetypes via Temporal Vehicle-Count Clustering
2. **visibility_count_correlation** — Disentangling Real Traffic Drops from Visibility Degradation in Urban CCTV Streams
3. **co2_proxy_heatmap** — A Camera-Derived Proxy for Hourly CO2 Emissions Across Bangkok Districts
4. **rolling_baseline_anomaly** — Near-Real-Time Traffic Anomaly Detection Using Rolling Hourly Baselines
5. **cross_camera_travel_time** — Estimating Inter-Intersection Travel Time from Count Cross-Correlation Across Adjacent CCTV Cameras

> Scores follow the AI Scientist schema: Interestingness, Feasibility, Novelty on a 1–10 scale; Score is the overall ML-conference-style rating (1–10). Full idea details in `ideas.json`.
