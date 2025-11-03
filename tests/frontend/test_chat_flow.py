import pytest
from playwright.sync_api import Page, expect
import time


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


def test_page_loads_with_greeting(page: Page):
    """Test that the chat page loads and shows Cat's greeting"""
    page.goto("http://localhost:3000/index.html")
    
    # Check that page title is correct
    expect(page).to_have_title("NsureCat - Chat with Cat")
    
    # Check that greeting message appears
    cat_message = page.locator('[data-testid="cat-message"]').first
    expect(cat_message).to_be_visible()
    expect(cat_message).to_contain_text("Hi! I'm Cat")
    
    # Check quick reply buttons appear
    quick_replies = page.locator('[data-testid="quick-replies"]')
    expect(quick_replies).to_be_visible()


def test_theme_toggle(page: Page):
    """Test theme toggle button switches between light and dark mode"""
    page.goto("http://localhost:3000/index.html")
    
    # Initial state should be light mode
    html = page.locator("html")
    expect(html).not_to_have_class("dark")
    
    # Click theme toggle
    page.click('[data-testid="theme-toggle-button"]')
    
    # Should now be dark mode
    expect(html).to_have_class("dark")
    
    # Click again to go back to light
    page.click('[data-testid="theme-toggle-button"]')
    expect(html).not_to_have_class("dark")


def test_user_can_type_message(page: Page):
    """Test that user can type and send a message"""
    page.goto("http://localhost:3000/index.html")
    
    # Type a message
    page.fill('[data-testid="user-input"]', "Hello Cat!")
    
    # Click send
    page.click('[data-testid="send-button"]')
    
    # Check user message appears
    user_message = page.locator('[data-testid="user-message"]').first
    expect(user_message).to_be_visible()
    expect(user_message).to_contain_text("Hello Cat!")
    
    # Input should be cleared
    expect(page.locator('[data-testid="user-input"]')).to_have_value("")


def test_policy_form_opens_and_closes(page: Page):
    """Test that policy form modal can be opened and closed"""
    page.goto("http://localhost:3000/index.html")
    
    # Click Form quick reply button
    page.click('text=Form')
    
    # Modal should be visible
    modal = page.locator('#policy-form-modal')
    expect(modal).to_be_visible()
    
    # Close modal
    page.click('#cancel-form')
    
    # Modal should be hidden
    expect(modal).not_to_be_visible()


def test_policy_form_validation(page: Page):
    """Test that policy form requires all fields"""
    page.goto("http://localhost:3000/index.html")
    
    # Open form
    page.click('text=Form')
    
    # Try to submit empty form
    submit_btn = page.locator('[data-testid="submit-policy-form"]')
    submit_btn.click()
    
    # Form should still be visible (validation failed)
    modal = page.locator('#policy-form-modal')
    expect(modal).to_be_visible()


def test_complete_chat_flow_with_mocked_apis(page: Page):
    """Test the complete user flow from policy input to payment"""
    
    # Mock backend APIs
    page.route("**/v1/shop", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"savings_6mo": 246.00, "new_carrier": "Rebel Mutual"}'
    ))
    
    page.route("**/v1/save", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"status": "success"}'
    ))
    
    page.route("**/api/text-to-speech", lambda route: route.fulfill(
        status=200,
        content_type="audio/mpeg",
        body=b"mock audio"
    ))
    
    page.goto("http://localhost:3000/index.html")
    
    # Step 1: Open policy form
    page.click('text=Form')
    
    # Step 2: Fill out form
    page.select_option('#state', 'NJ')
    page.select_option('#carrier', 'Geico')
    page.fill('#amount', '975')
    page.select_option('#bodily_injury', '100/300')
    page.select_option('#property_damage', '50000')
    page.select_option('#uninsured_motorist', '50/100')
    page.select_option('#collision', '500')
    page.select_option('#comprehensive', '500')
    page.select_option('#personal_injury_protection', '50000')
    
    # Step 3: Submit form
    page.click('[data-testid="submit-policy-form"]')
    
    # Wait for modal to close
    time.sleep(0.5)
    
    # Step 4: Check summary message appears
    expect(page.locator('text=I see you have')).to_be_visible()
    
    # Step 5: Wait for results (loading spinner should appear and disappear)
    expect(page.locator('#loading-spinner')).to_be_visible()
    page.wait_for_selector('#loading-spinner', state='hidden', timeout=10000)
    
    # Step 6: Check result card appears
    result_card = page.locator('[data-testid="result-card"]')
    expect(result_card).to_be_visible()
    expect(result_card).to_contain_text("Rebel Mutual")
    expect(result_card).to_contain_text("$246.00")
    
    # Step 7: Click choose button (will open wallet modal in real scenario)
    # Note: Wallet connection requires MetaMask which we can't test in headless


def test_error_handling_api_failure(page: Page):
    """Test that API errors are handled gracefully"""
    
    # Mock API to return error
    page.route("**/v1/shop", lambda route: route.fulfill(
        status=500,
        content_type="application/json",
        body='{"detail": "Internal server error"}'
    ))
    
    page.goto("http://localhost:3000/index.html")
    
    # Open and fill form
    page.click('text=Form')
    page.select_option('#state', 'NJ')
    page.select_option('#carrier', 'Geico')
    page.fill('#amount', '975')
    page.select_option('#bodily_injury', '100/300')
    page.select_option('#property_damage', '50000')
    page.select_option('#uninsured_motorist', '50/100')
    page.select_option('#collision', '500')
    page.select_option('#comprehensive', '500')
    page.select_option('#personal_injury_protection', '50000')
    
    # Submit
    page.click('[data-testid="submit-policy-form"]')
    
    # Wait for API call
    time.sleep(1)
    
    # Error toast should appear
    error_toast = page.locator('#error-toast')
    expect(error_toast).to_be_visible()
    expect(error_toast).to_contain_text("Server error")
    
    # Cat should show error message
    expect(page.locator('text=trouble reaching the carriers')).to_be_visible()


def test_voice_button_visibility(page: Page):
    """Test that voice button is present"""
    page.goto("http://localhost:3000/index.html")
    
    voice_btn = page.locator('[data-testid="voice-button"]')
    expect(voice_btn).to_be_visible()


def test_responsive_design_mobile(page: Page):
    """Test that page works on mobile viewport"""
    # Set mobile viewport
    page.set_viewport_size({"width": 375, "height": 667})
    
    page.goto("http://localhost:3000/index.html")
    
    # Check that elements are still visible
    expect(page.locator('.header-navbar')).to_be_visible()
    expect(page.locator('[data-testid="cat-message"]').first).to_be_visible()
    expect(page.locator('[data-testid="user-input"]')).to_be_visible()
    expect(page.locator('[data-testid="send-button"]')).to_be_visible()


def test_wallet_modal_opens(page: Page):
    """Test wallet modal can be opened (requires result selection first)"""
    # Mock API
    page.route("**/v1/shop", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"savings_6mo": 246.00, "new_carrier": "Rebel Mutual"}'
    ))
    
    page.goto("http://localhost:3000/index.html")
    
    # Complete flow to get to wallet step
    page.click('text=Form')
    page.select_option('#state', 'NJ')
    page.select_option('#carrier', 'Geico')
    page.fill('#amount', '975')
    page.select_option('#bodily_injury', '100/300')
    page.select_option('#property_damage', '50000')
    page.select_option('#uninsured_motorist', '50/100')
    page.select_option('#collision', '500')
    page.select_option('#comprehensive', '500')
    page.select_option('#personal_injury_protection', '50000')
    page.click('[data-testid="submit-policy-form"]')
    
    # Wait for result
    page.wait_for_selector('[data-testid="result-card"]', state='visible', timeout=10000)
    
    # Click choose button
    page.click('[data-testid="choose-result-btn"]')
    
    # Wallet modal should open
    wallet_modal = page.locator('#wallet-modal')
    expect(wallet_modal).to_be_visible()
    
    # Check wallet options are present
    expect(page.locator('[data-testid="connect-metamask"]')).to_be_visible()
    expect(page.locator('[data-testid="connect-circle"]')).to_be_visible()


def test_localstorage_persistence(page: Page):
    """Test that chat history is saved to localStorage"""
    page.goto("http://localhost:3000/index.html")
    
    # Send a message
    page.fill('[data-testid="user-input"]', "Test message")
    page.click('[data-testid="send-button"]')
    
    # Check localStorage
    storage = page.evaluate("() => localStorage.getItem('nsurecat_chat_history')")
    assert storage is not None
    assert "Test message" in storage


def test_accessibility_aria_labels(page: Page):
    """Test that important elements have ARIA labels"""
    page.goto("http://localhost:3000/index.html")
    
    # Check key interactive elements have aria-label
    theme_btn = page.locator('[data-testid="theme-toggle-button"]')
    expect(theme_btn).to_have_attribute('aria-label', 'Toggle theme')
    
    user_input = page.locator('[data-testid="user-input"]')
    expect(user_input).to_have_attribute('aria-label', 'Message input')
    
    voice_btn = page.locator('[data-testid="voice-button"]')
    expect(voice_btn).to_have_attribute('aria-label', 'Use voice input')


# Integration tests (require backend to be running)
@pytest.mark.integration
def test_real_api_shop_endpoint(page: Page):
    """Test with real backend API (requires backend running)"""
    page.goto("http://localhost:3000/index.html")
    
    # Open and fill form
    page.click('text=Form')
    page.select_option('#state', 'NJ')
    page.select_option('#carrier', 'Geico')
    page.fill('#amount', '975')
    page.select_option('#bodily_injury', '100/300')
    page.select_option('#property_damage', '50000')
    page.select_option('#uninsured_motorist', '50/100')
    page.select_option('#collision', '500')
    page.select_option('#comprehensive', '500')
    page.select_option('#personal_injury_protection', '50000')
    
    # Submit
    page.click('[data-testid="submit-policy-form"]')
    
    # Wait for result (real API)
    result_card = page.wait_for_selector('[data-testid="result-card"]', timeout=15000)
    expect(result_card).to_be_visible()
    
    # Should have carrier name and savings
    expect(result_card).to_contain_text("$")


    # Check agent animation and results
    expect(page.locator('[data-testid="agent-animation"]')).to_be_visible()
    page.wait_for_selector('[data-testid="results-bubble"]')
    expect(page.locator('[data-testid="results-bubble"]')).to_contain_text("Rebel Mutual: Save $246.00")

    # Select result
    page.click('[data-testid="select-result-button"]')

    # Wallet modal
    expect(page.locator('[data-testid="wallet-modal"]')).to_be_visible()
    # Mock MetaMask
    page.evaluate("window.ethereum = { request: () => Promise.resolve(['0x123']) }")
    page.click('[data-testid="connect-wallet-button"]')
    page.click('[data-testid="confirm-payment-button"]')

    # Success
    expect(page.locator('[data-testid="chat-bubble"]')).to_contain_text("You have saved")


def test_form_validation_missing_fields(page: Page):
    page.goto("http://localhost:3000/")
    page.click('[data-testid="form-input-button"]')
    page.click('[data-testid="submit-form-button"]')
    expect(page.locator('[data-testid="error-toast"]')).to_contain_text("This field is required")


def test_api_error_shop_fails(page: Page):
    page.route("**/v1/shop", lambda route: route.fulfill(
        status=500,
        body='{"detail": "Server error"}'
    ))
    page.goto("http://localhost:3000/")
    page.click('[data-testid="form-input-button"]')
    # Fill form minimally
    page.select_option('[data-testid="bodily-injury-dropdown"]', '100/300')
    page.select_option('[data-testid="property-damage-dropdown"]', '50/100')
    page.select_option('[data-testid="uninsured-motorist-dropdown"]', '25/50')
    page.select_option('[data-testid="collision-dropdown"]', '500')
    page.select_option('[data-testid="comprehensive-dropdown"]', '500')
    page.select_option('[data-testid="personal-injury-protection-dropdown"]', '10/20')
    page.click('[data-testid="submit-form-button"]')
    expect(page.locator('[data-testid="chat-bubble"]')).to_contain_text("Server error")


def test_voice_input_unsupported_browser(page: Page):
    page.evaluate("delete window.webkitSpeechRecognition")
    page.goto("http://localhost:3000/")
    page.click('[data-testid="voice-input-button"]')
    expect(page.locator('[data-testid="voice-input-button"]')).to_be_disabled()
    expect(page.locator('[data-testid="error-toast"]')).to_contain_text("Voice input not supported")


def test_theme_toggle(page: Page):
    page.goto("http://localhost:3000/")
    page.click('[data-testid="theme-toggle-button"]')
    expect(page.locator('html')).to_have_class("dark")
    # Check persistence
    page.reload()
    expect(page.locator('html')).to_have_class("dark")


def test_responsive_mobile_view(page: Page):
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto("http://localhost:3000/")
    expect(page.locator('[data-testid="chat-container"]')).to_have_css("max-width", "100%")


def test_wallet_metamask_not_detected(page: Page):
    page.goto("http://localhost:3000/")
    # Simulate reaching wallet modal
    page.click('[data-testid="form-input-button"]')
    # Fill and submit to get to results
    page.select_option('[data-testid="bodily-injury-dropdown"]', '100/300')
    page.select_option('[data-testid="property-damage-dropdown"]', '50/100')
    page.select_option('[data-testid="uninsured-motorist-dropdown"]', '25/50')
    page.select_option('[data-testid="collision-dropdown"]', '500')
    page.select_option('[data-testid="comprehensive-dropdown"]', '500')
    page.select_option('[data-testid="personal-injury-protection-dropdown"]', '10/20')
    page.click('[data-testid="submit-form-button"]')
    page.wait_for_selector('[data-testid="results-bubble"]')
    page.click('[data-testid="select-result-button"]')
    page.evaluate("delete window.ethereum")
    page.click('[data-testid="connect-wallet-button"]')
    expect(page.locator('[data-testid="error-toast"]')).to_contain_text("MetaMask not detected")