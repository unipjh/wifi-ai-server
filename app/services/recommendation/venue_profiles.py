VENUE_PROFILE: dict[str, dict] = {
    "학술정보원_4층_열람실": {
        "lat": 37.551629, "lng": 127.074318,
        "floor_m": 12.0,  # 4층: (4-1)*4m
        "quiet": 1.0, "solo": 1.0, "team": 0.1,
        "p_focus": 1.0, "p_team": 0.0, "p_casual": 0.2,
    },
    "학생회관_5층_동아리방": {
        "lat": 37.549508, "lng": 127.075110,
        "floor_m": 16.0,  # 5층: (5-1)*4m
        "quiet": 0.3, "solo": 0.3, "team": 0.9,
        "p_focus": 0.3, "p_team": 1.0, "p_casual": 0.7,
    },
    "광개토관_15층_카페": {
        "lat": 37.550294, "lng": 127.073174,
        "floor_m": 56.0,  # 15층: (15-1)*4m
        "quiet": 0.4, "solo": 0.5, "team": 0.7,
        "p_focus": 0.4, "p_team": 0.6, "p_casual": 0.8,
    },
    "AI센터_1층_카페": {
        "lat": 37.551105, "lng": 127.075750,
        "floor_m": 0.0,  # 1층: 기준
        "quiet": 0.5, "solo": 0.5, "team": 0.6,
        "p_focus": 0.4, "p_team": 0.5, "p_casual": 0.9,
    },
    "AI센터_4층_과방": {
        "lat": 37.551105, "lng": 127.075750,
        "floor_m": 12.0,  # 4층: (4-1)*4m
        "quiet": 0.6, "solo": 0.4, "team": 0.8,
        "p_focus": 0.5, "p_team": 0.9, "p_casual": 0.4,
    },
    "광개토관_B1_카페": {
        "lat": 37.550294, "lng": 127.073174,
        "floor_m": 4.0,  # B1: 지하 1층
        "quiet": 0.5, "solo": 0.5, "team": 0.6,
        "p_focus": 0.4, "p_team": 0.5, "p_casual": 0.9,
    },
    "광개토관_7층_라운지": {
        "lat": 37.550294, "lng": 127.073174,
        "floor_m": 24.0,  # 7층: (7-1)*4m
        "quiet": 0.7, "solo": 0.7, "team": 0.5,
        "p_focus": 0.5, "p_team": 0.4, "p_casual": 0.7,
    },
    "학술정보원_2층_라운지&카페": {
        "lat": 37.551629, "lng": 127.074318,
        "floor_m": 4.0,  # 2층: (2-1)*4m
        "quiet": 0.6, "solo": 0.6, "team": 0.5,
        "p_focus": 0.6, "p_team": 0.4, "p_casual": 0.8,
    },
    "학생회관_2층_카페": {
        "lat": 37.549508, "lng": 127.075110,
        "floor_m": 4.0,  # 2층: (2-1)*4m
        "quiet": 0.5, "solo": 0.6, "team": 0.6,
        "p_focus": 0.3, "p_team": 0.5, "p_casual": 0.9,
    },
    "충무관_1층_카페": {
        "lat": 37.552279, "lng": 127.073956,
        "floor_m": 0.0,  # 1층: 기준
        "quiet": 0.5, "solo": 0.5, "team": 0.6,
        "p_focus": 0.4, "p_team": 0.5, "p_casual": 0.8,
    },
}

AVAILABILITY: dict[str, dict[str, float]] = {
    "학술정보원_4층_열람실": {
        "WD_AM": 1.0, "WD_PEAK": 1.0, "WD_PM": 1.0, "WD_NIGHT": 0.8,
        "WE_AM": 0.9, "WE_PEAK": 0.9, "WE_PM": 0.9, "WE_NIGHT": 0.0,
    },
    "학생회관_5층_동아리방": {
        "WD_AM": 0.5, "WD_PEAK": 0.7, "WD_PM": 0.8, "WD_NIGHT": 0.6,
        "WE_AM": 0.3, "WE_PEAK": 0.5, "WE_PM": 0.6, "WE_NIGHT": 0.4,
    },
    "광개토관_15층_카페": {
        "WD_AM": 0.8, "WD_PEAK": 1.0, "WD_PM": 0.9, "WD_NIGHT": 0.0,
        "WE_AM": 0.5, "WE_PEAK": 0.7, "WE_PM": 0.6, "WE_NIGHT": 0.0,
    },
    "AI센터_1층_카페": {
        "WD_AM": 0.7, "WD_PEAK": 1.0, "WD_PM": 0.8, "WD_NIGHT": 0.0,
        "WE_AM": 0.4, "WE_PEAK": 0.6, "WE_PM": 0.5, "WE_NIGHT": 0.0,
    },
    "AI센터_4층_과방": {
        "WD_AM": 0.5, "WD_PEAK": 0.7, "WD_PM": 0.7, "WD_NIGHT": 0.5,
        "WE_AM": 0.2, "WE_PEAK": 0.3, "WE_PM": 0.4, "WE_NIGHT": 0.2,
    },
    "광개토관_B1_카페": {
        "WD_AM": 0.7, "WD_PEAK": 1.0, "WD_PM": 0.9, "WD_NIGHT": 0.0,
        "WE_AM": 0.0, "WE_PEAK": 0.0, "WE_PM": 0.0, "WE_NIGHT": 0.0,
    },
    "광개토관_7층_라운지": {
        "WD_AM": 0.6, "WD_PEAK": 0.9, "WD_PM": 0.7, "WD_NIGHT": 0.0,
        "WE_AM": 0.3, "WE_PEAK": 0.5, "WE_PM": 0.4, "WE_NIGHT": 0.0,
    },
    "학술정보원_2층_라운지&카페": {
        "WD_AM": 0.8, "WD_PEAK": 1.0, "WD_PM": 0.9, "WD_NIGHT": 0.5,
        "WE_AM": 0.7, "WE_PEAK": 0.9, "WE_PM": 0.8, "WE_NIGHT": 0.0,
    },
    "학생회관_2층_카페": {
        "WD_AM": 0.7, "WD_PEAK": 1.0, "WD_PM": 0.8, "WD_NIGHT": 0.0,
        "WE_AM": 0.5, "WE_PEAK": 0.7, "WE_PM": 0.6, "WE_NIGHT": 0.0,
    },
    "충무관_1층_카페": {
        "WD_AM": 0.7, "WD_PEAK": 1.0, "WD_PM": 0.8, "WD_NIGHT": 0.0,
        "WE_AM": 0.0, "WE_PEAK": 0.0, "WE_PM": 0.0, "WE_NIGHT": 0.0,
    },
}
