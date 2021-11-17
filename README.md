# Vaccine API test

## Test for: WCG

## Test Endpoint: /report_taken

| Test  | Description | Status |
| ----------- | ----------- | --- |
| test_report_sent | Test report successfully sent for walk-in. | P |
| test_not_enough_key | Test missing query parameter. | P |
| test_invalid_vaccine_name | Test invalid vaccine name input. | P |
| test_unregistered_id | Test report send from unregistered citizen ID.| P |
| test_invalid_id | Test invalid citizen ID. | P |
| test_report_available_vaccine | Test report for second dose vaccine. | P |
| test_report_unavailable_vaccine | Test report for second dose vaccine with invalid vaccination orders. | P |
| test_empty_second_dose | Test sending invalid second dose. | P |
| test_is_reserved | Test when already registered citizen request as a walk-in. | P |
| test_reserve_option | Test report taken from reserved citizen successfully. | P |
