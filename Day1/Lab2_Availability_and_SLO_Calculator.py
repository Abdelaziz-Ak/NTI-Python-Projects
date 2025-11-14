total_requests = 1000
failed_requests = 1
slo_target = 99.9

if total_requests == 0:
    availability = 100.0
else:
    availability = (1- (failed_requests/total_requests))*100 #TODO: Calculate availability as a percentage

meets_slo = availability >= slo_target #TODO: Determine if availability meets the SLO target

error_budget_total = 100 - slo_target #TODO: Calculate total error budget based on SLO target
error_budget_used = 100 - availability #TODO: Calculate used error budget based on availability
error_budget_remaining = error_budget_total - error_budget_used #TODO: Calculate remaining error budget


print(f"Availability: {availability:.3f}%")
print(f"Meets SLO {slo_target}%? {meets_slo}")
print(f"Error budget used: {error_budget_used}%")
print(f"Error budget remaining: {max(error_budget_remaining, 0)}%")


