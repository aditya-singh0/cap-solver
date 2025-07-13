#!/usr/bin/env python3
"""
UPI QR Code Setup Script
This script helps you add your UPI QR code to the payment modal.
"""

import os
import shutil
from pathlib import Path

def print_status(message):
    print(f"🔄 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def setup_upi_qr():
    """Set up UPI QR code for payments"""
    print("💰 UPI QR Code Setup")
    print("=" * 30)
    
    # Create assets directory if it doesn't exist
    assets_dir = Path("frontend/assets")
    assets_dir.mkdir(exist_ok=True)
    
    print_status("Setting up UPI payment integration...")
    
    # Check if QR code image exists
    qr_files = list(assets_dir.glob("*.png")) + list(assets_dir.glob("*.jpg")) + list(assets_dir.glob("*.jpeg"))
    
    if qr_files:
        print_success(f"Found QR code image: {qr_files[0].name}")
        qr_path = qr_files[0]
    else:
        print_warning("No QR code image found in frontend/assets/")
        print("Please add your UPI QR code image to frontend/assets/")
        print("Supported formats: PNG, JPG, JPEG")
        return False
    
    # Get UPI details from user
    print("\n📱 Enter your UPI payment details:")
    upi_id = input("UPI ID (e.g., yourname@bank): ").strip()
    name = input("Name (as shown in UPI): ").strip()
    
    if not upi_id or not name:
        print_warning("UPI ID and Name are required!")
        return False
    
    # Update the HTML with actual UPI details
    update_html_with_upi(qr_path.name, upi_id, name)
    
    print_success("UPI QR code setup completed!")
    print(f"📱 UPI ID: {upi_id}")
    print(f"👤 Name: {name}")
    print(f"🖼️  QR Code: {qr_path.name}")
    
    return True

def update_html_with_upi(qr_filename, upi_id, name):
    """Update the HTML file with actual UPI details"""
    html_file = Path("frontend/index.html")
    
    if not html_file.exists():
        print_warning("frontend/index.html not found!")
        return False
    
    # Read the HTML file
    content = html_file.read_text()
    
    # Replace placeholder QR code with actual image
    qr_placeholder = '''<div class="w-48 h-48 mx-auto bg-white rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center">
                            <div class="text-center">
                                <i class="fas fa-qrcode text-6xl text-gray-400 mb-2"></i>
                                <p class="text-sm text-gray-500">Your UPI QR Code</p>
                                <p class="text-xs text-gray-400 mt-1">Upload your QR image here</p>
                            </div>
                        </div>'''
    
    qr_image = f'''<img src="assets/{qr_filename}" alt="UPI QR Code" class="w-48 h-48 mx-auto rounded-lg shadow-lg">'''
    
    content = content.replace(qr_placeholder, qr_image)
    
    # Replace placeholder UPI details
    content = content.replace('UPI ID: your-upi@bank', f'UPI ID: {upi_id}')
    content = content.replace('Name: Your Name', f'Name: {name}')
    
    # Add copy UPI ID functionality
    copy_script = f'''
                    <button class="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors" onclick="copyUpiId('{upi_id}')">
                        <i class="fas fa-copy mr-2"></i>Copy UPI ID
                    </button>'''
    
    content = content.replace('<button class="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">\n                        <i class="fas fa-copy mr-2"></i>Copy UPI ID\n                    </button>', copy_script)
    
    # Add copy function to JavaScript
    copy_function = '''
        // Function to copy UPI ID
        function copyUpiId(upiId) {
            navigator.clipboard.writeText(upiId).then(function() {
                showNotification('UPI ID copied to clipboard!', 'success');
            }, function(err) {
                showNotification('Failed to copy UPI ID', 'error');
            });
        }'''
    
    # Find the end of the script tag and add the function
    script_end = content.find('</script>')
    if script_end != -1:
        content = content[:script_end] + copy_function + '\n    ' + content[script_end:]
    
    # Write the updated content
    html_file.write_text(content)
    
    print_success("HTML file updated with UPI details!")

def main():
    """Main setup function"""
    print("💰 Captcha Solver SaaS - UPI Payment Setup")
    print("=" * 50)
    
    # Check if frontend directory exists
    if not Path("frontend").exists():
        print_warning("Frontend directory not found!")
        print("Please run this script from the project root directory.")
        return
    
    # Setup UPI QR code
    if setup_upi_qr():
        print("\n🎉 UPI payment setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Test the payment modal by clicking 'Upgrade' on any plan")
        print("2. Verify the QR code displays correctly")
        print("3. Test the 'Copy UPI ID' functionality")
        print("4. Deploy your application")
    else:
        print("\n❌ UPI setup failed. Please check the requirements above.")

if __name__ == "__main__":
    main() 