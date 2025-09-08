# //functions/optimization_engine_functions.py
# [Version 08-09-2025 14:45:00]
# Optimization Recommendation Engine Functions for TaxOptim AI (MVP Version)
# Authored by: Sotiris Spyrou, CEO, VerityAI

import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class OptimizationPriority(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

@dataclass
class OptimizationRecommendation:
    """Individual optimization recommendation"""
    id: str
    category: str
    title: str
    description: str
    potential_saving: float
    priority: OptimizationPriority
    deadline: Optional[str]
    next_steps: List[str]
    requirements: List[str]

class TaxOptimizationEngine:
    """Tax optimization recommendation engine"""
    
    def __init__(self):
        pass
    
    def generate_optimization_recommendations(self, tax_data: Dict, user_profile: Dict = None) -> Dict:
        """Generate comprehensive optimization recommendations"""
        
        recommendations = []
        
        # Immediate optimization opportunities
        immediate_opportunities = self._identify_immediate_opportunities(tax_data)
        recommendations.extend(immediate_opportunities)
        
        # Pension optimization
        pension_recommendations = self._analyze_pension_optimization(tax_data)
        recommendations.extend(pension_recommendations)
        
        # Investment optimization
        investment_recommendations = self._analyze_investment_optimization(tax_data)
        recommendations.extend(investment_recommendations)
        
        # Prioritize recommendations
        prioritized_recommendations = self._prioritize_recommendations(recommendations)
        
        return {
            "optimization_summary": self._generate_optimization_summary(prioritized_recommendations),
            "immediate_actions": [r for r in prioritized_recommendations if r.priority in [OptimizationPriority.CRITICAL, OptimizationPriority.HIGH]],
            "all_recommendations": prioritized_recommendations,
            "implementation_roadmap": self._generate_implementation_roadmap(prioritized_recommendations)
        }
    
    def _identify_immediate_opportunities(self, tax_data: Dict) -> List[OptimizationRecommendation]:
        """Identify immediate tax year optimization opportunities"""
        
        recommendations = []
        total_liability = tax_data.get('total_liability', {})
        income_tax = total_liability.get('income_tax', 0)
        
        # Pension contribution opportunity
        if income_tax > 1000:
            potential_saving = min(income_tax * 0.4, 24000)
            
            recommendations.append(OptimizationRecommendation(
                id="PENSION_2024_25",
                category="Pension Contributions",
                title="Optimize 2024/25 Pension Contributions",
                description="Maximize pension contributions before April 5th to reduce current year tax liability",
                potential_saving=potential_saving,
                priority=OptimizationPriority.HIGH,
                deadline="2025-04-05",
                next_steps=[
                    "Calculate maximum allowable contribution",
                    "Contact pension provider",
                    "Set up payment before April 5th"
                ],
                requirements=["Available cash", "Pension scheme access"]
            ))
        
        # ISA contribution opportunity
        recommendations.append(OptimizationRecommendation(
            id="ISA_2024_25",
            category="Tax-Free Investments",
            title="Maximize ISA Allowance",
            description="Use remaining ISA allowance for tax-free investment growth",
            potential_saving=0,  # Long-term benefit
            priority=OptimizationPriority.MEDIUM,
            deadline="2025-04-05",
            next_steps=[
                "Check current ISA usage",
                "Transfer available funds to ISA",
                "Consider investment options"
            ],
            requirements=["Available cash", "ISA provider"]
        ))
        
        return recommendations
    
    def _analyze_pension_optimization(self, tax_data: Dict) -> List[OptimizationRecommendation]:
        """Analyze pension contribution optimization strategies"""
        
        recommendations = []
        
        # Current pension contributions
        current_contributions = tax_data.get('tax_calculations', {}).get('income_tax', {}).get('pension_contributions', 0)
        total_income = tax_data.get('tax_calculations', {}).get('income_tax', {}).get('gross_income', 0)
        
        # Calculate optimal contribution level
        max_annual_allowance = 60000
        available_allowance = max_annual_allowance - current_contributions
        
        if available_allowance > 1000 and total_income > 50000:
            recommendations.append(OptimizationRecommendation(
                id="PENSION_OPTIMIZATION",
                category="Pension Planning",
                title="Increase Pension Contributions",
                description=f"Additional pension contributions could provide significant tax relief",
                potential_saving=available_allowance * 0.4,
                priority=OptimizationPriority.HIGH,
                deadline="2025-04-05",
                next_steps=[
                    "Review current pension arrangements",
                    "Calculate optimal contribution level",
                    "Arrange additional contributions"
                ],
                requirements=["Available funds", "Pension scheme capacity"]
            ))
        
        return recommendations
    
    def _analyze_investment_optimization(self, tax_data: Dict) -> List[OptimizationRecommendation]:
        """Analyze investment structure optimization"""
        
        recommendations = []
        
        # Check dividend income
        dividend_data = tax_data.get('income_breakdown', {}).get('dividends', {})
        if isinstance(dividend_data, dict):
            dividend_income = dividend_data.get('dividend_income', 0)
            
            if dividend_income > 1000:  # Above dividend allowance
                recommendations.append(OptimizationRecommendation(
                    id="INVESTMENT_STRUCTURE",
                    category="Investment Optimization",
                    title="Optimize Investment Structure",
                    description="Consider tax-efficient investment wrappers to reduce dividend tax",
                    potential_saving=dividend_income * 0.0875,
                    priority=OptimizationPriority.MEDIUM,
                    deadline=None,
                    next_steps=[
                        "Review current investment holdings",
                        "Consider ISA transfers",
                        "Evaluate pension vs ISA strategies"
                    ],
                    requirements=["Investment portfolio review"]
                ))
        
        return recommendations
    
    def _prioritize_recommendations(self, recommendations: List[OptimizationRecommendation]) -> List[OptimizationRecommendation]:
        """Prioritize recommendations based on impact and deadlines"""
        
        def priority_score(rec: OptimizationRecommendation) -> float:
            base_score = rec.potential_saving / 10000  # Normalize to £10k
            deadline_bonus = 0.5 if rec.deadline == "2025-04-05" else 0.0
            return base_score + deadline_bonus
        
        return sorted(recommendations, key=priority_score, reverse=True)
    
    def _generate_implementation_roadmap(self, recommendations: List[OptimizationRecommendation]) -> Dict:
        """Generate implementation roadmap with timeline"""
        
        roadmap = {
            "immediate_actions": [],
            "medium_term_actions": []
        }
        
        for rec in recommendations:
            if rec.deadline == "2025-04-05":
                roadmap["immediate_actions"].append({
                    "title": rec.title,
                    "deadline": rec.deadline,
                    "next_steps": rec.next_steps[:2]
                })
            else:
                roadmap["medium_term_actions"].append({
                    "title": rec.title,
                    "category": rec.category,
                    "requirements": rec.requirements
                })
        
        return roadmap
    
    def _generate_optimization_summary(self, recommendations: List[OptimizationRecommendation]) -> Dict:
        """Generate high-level optimization summary"""
        
        total_potential_savings = sum(r.potential_saving for r in recommendations)
        high_priority_count = len([r for r in recommendations if r.priority == OptimizationPriority.HIGH])
        
        return {
            "total_potential_savings": total_potential_savings,
            "immediate_opportunities": high_priority_count,
            "strategies_identified": len(recommendations),
            "implementation_timeline": "Immediate to 12 months"
        }

def generate_comprehensive_optimization_plan(tax_calculation_result: Dict, user_preferences: Dict = None) -> Dict:
    """Generate complete optimization plan with recommendations"""
    
    optimizer = TaxOptimizationEngine()
    optimization_results = optimizer.generate_optimization_recommendations(
        tax_calculation_result, user_preferences
    )
    
    return {
        "optimization_date": datetime.now().isoformat(),
        "tax_year": "2024/25",
        "optimization_results": optimization_results,
        "summary": {
            "total_recommendations": len(optimization_results["all_recommendations"]),
            "immediate_actions": len(optimization_results["immediate_actions"]),
            "potential_savings": optimization_results["optimization_summary"]["total_potential_savings"]
        }
    }
