"""
Data handling utilities for Ethiopia Financial Inclusion project.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class DataHandler:
    """Handles loading, processing, and saving financial inclusion data."""
    
    def __init__(self, raw_data_path: str = "data/raw/ethiopia_fi_unified_data.csv",
                 ref_data_path: str = "data/raw/reference_codes.csv"):
        self.raw_data_path = raw_data_path
        self.ref_data_path = ref_data_path
        self.df = None
        self.ref_df = None
        
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load main data and reference codes."""
        self.df = pd.read_csv(self.raw_data_path)
        self.ref_df = pd.read_csv(self.ref_data_path)
        print(f"✅ Data loaded: {self.df.shape[0]} records, {self.df.shape[1]} columns")
        print(f"✅ Reference codes: {self.ref_df.shape[0]} codes")
        return self.df, self.ref_df
    
    def get_record_type_summary(self) -> pd.DataFrame:
        """Get summary statistics by record type."""
        if self.df is None:
            self.load_data()
        
        summary = {
            'record_type': [],
            'count': [],
            'pillars': [],
            'indicators': [],
            'date_range': []
        }
        
        for rt in self.df['record_type'].unique():
            rt_df = self.df[self.df['record_type'] == rt]
            summary['record_type'].append(rt)
            summary['count'].append(len(rt_df))
            
            # Get unique pillars
            if 'pillar' in rt_df.columns:
                pillars = rt_df['pillar'].dropna().unique()
                summary['pillars'].append(', '.join(pillars[:3]) + ('...' if len(pillars) > 3 else ''))
            else:
                summary['pillars'].append('N/A')
            
            # Get unique indicators
            if 'indicator' in rt_df.columns:
                indicators = rt_df['indicator'].dropna().unique()
                summary['indicators'].append(len(indicators))
            else:
                summary['indicators'].append(0)
            
            # Get date range
            if 'observation_date' in rt_df.columns:
                dates = pd.to_datetime(rt_df['observation_date'], errors='coerce')
                valid_dates = dates.dropna()
                if not valid_dates.empty:
                    date_range = f"{valid_dates.min().date()} to {valid_dates.max().date()}"
                else:
                    date_range = 'N/A'
                summary['date_range'].append(date_range)
            else:
                summary['date_range'].append('N/A')
        
        return pd.DataFrame(summary)
    
    def filter_by_pillar(self, pillar: str) -> pd.DataFrame:
        """Filter observations by pillar."""
        if self.df is None:
            self.load_data()
        
        mask = (self.df['record_type'] == 'observation') & (self.df['pillar'] == pillar)
        return self.df[mask].copy()
    
    def get_events_with_impacts(self) -> pd.DataFrame:
        """Get events with their associated impact links."""
        if self.df is None:
            self.load_data()
        
        # Get events
        events = self.df[self.df['record_type'] == 'event'].copy()
        
        # Get impact links
        impacts = self.df[self.df['record_type'] == 'impact_link'].copy()
        
        # Merge
        if not impacts.empty and not events.empty:
            merged = pd.merge(
                impacts,
                events[['record_id', 'indicator', 'observation_date', 'category']],
                left_on='parent_id',
                right_on='record_id',
                suffixes=('_impact', '_event')
            )
            return merged
        return pd.DataFrame()
    
    def add_records(self, new_records: List[Dict], record_type: str) -> pd.DataFrame:
        """Add new records to the dataset following the schema.
        
        Args:
            new_records: List of dictionaries with record data
            record_type: Type of records ('observation', 'event', 'impact_link', 'target')
        """
        if self.df is None:
            self.load_data()
        
        # Convert to DataFrame
        new_df = pd.DataFrame(new_records)
        new_df['record_type'] = record_type
        
        # Add record_id if not present
        if 'record_id' not in new_df.columns:
            # Generate IDs based on existing ones
            existing_ids = self.df['record_id'].dropna()
            prefix_map = {
                'observation': 'OBS',
                'event': 'EVT',
                'impact_link': 'IMP',
                'target': 'TGT'
            }
            prefix = prefix_map.get(record_type, 'REC')
            
            # Find the next available number
            existing_nums = []
            for id_str in existing_ids:
                if id_str.startswith(prefix):
                    try:
                        num = int(id_str.split('_')[1])
                        existing_nums.append(num)
                    except:
                        pass
            
            next_num = max(existing_nums) + 1 if existing_nums else 1
            
            new_ids = [f"{prefix}_{next_num + i:04d}" for i in range(len(new_df))]
            new_df['record_id'] = new_ids
        
        # Append to main dataframe
        self.df = pd.concat([self.df, new_df], ignore_index=True)
        
        print(f"✅ Added {len(new_df)} new {record_type} records")
        return self.df
    
    def save_enriched_data(self, output_path: str = "data/processed/ethiopia_fi_enriched.csv"):
        """Save the enriched dataset."""
        if self.df is None:
            print("⚠️ No data loaded")
            return
        
        self.df.to_csv(output_path, index=False)
        print(f"✅ Enriched data saved to {output_path}")
        print(f"   Total records: {len(self.df)}")
        
        # Summary of additions
        original = pd.read_csv(self.raw_data_path)
        added = len(self.df) - len(original)
        print(f"   Added {added} new records")
        
        return self.df


def validate_record(record: Dict, record_type: str) -> List[str]:
    """Validate a record against schema requirements.
    
    Returns:
        List of validation errors
    """
    errors = []
    
    # Required fields by record type
    required_fields = {
        'observation': ['pillar', 'indicator', 'value_numeric', 'observation_date'],
        'event': ['category', 'indicator', 'observation_date'],
        'impact_link': ['parent_id', 'pillar', 'related_indicator'],
        'target': ['pillar', 'indicator', 'value_numeric', 'observation_date']
    }
    
    # Check required fields
    if record_type in required_fields:
        for field in required_fields[record_type]:
            if field not in record or pd.isna(record.get(field)):
                errors.append(f"Missing required field: {field}")
    
    # Record type specific validations
    if record_type == 'event' and 'pillar' in record and pd.notna(record.get('pillar')):
        errors.append("Event records should not have a pillar (it's assigned via impact_links)")
    
    return errors