import socket
from config.config import ports
import ipaddress
import requests
import ssl
import time
from datetime import datetime
from tools.gobuster_scan import run_gobuster_scan


def is_ip_address(input_string):
    try:
        ipaddress.ip_address(input_string)
        return True
    except ValueError:
        return False

def check_protocol(url_without_scheme):
    try:
        https_url = f"https://{url_without_scheme}"
        response = requests.head(https_url, allow_redirects=True, timeout=5)
        if response.status_code < 400: # Check for successful status codes
            return True
    except requests.exceptions.RequestException:
        pass
    try:
        http_url = f"http://{url_without_scheme}"
        response = requests.head(http_url, allow_redirects=True, timeout=5)
        if response.status_code < 400:
            return True
    except requests.exceptions.RequestException:
        pass

    return None
def grab_http_banner(url, timeout=5):
    """Grab HTTP headers and service information"""
    try:
        start_time = time.time()
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        response_time = time.time() - start_time
        
        headers = dict(response.headers)
        
        return {
            "headers": headers,
            "server": headers.get('Server', 'Unknown'),
            "x_powered_by": headers.get('X-Powered-By', 'Unknown'),
            "response_time": round(response_time, 3),
            "status_code": response.status_code,
            "content_type": headers.get('Content-Type', 'Unknown'),
            "content_length": headers.get('Content-Length', 'Unknown')
        }
    except Exception as e:
        return {"error": str(e)}

def grab_ftp_banner(target: str, port: int):
    """Grab FTP banner"""
    try:
        start_time = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((target, port))
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        response_time = time.time() - start_time
        sock.close()
        return {
            "banner": banner,
            "service": "FTP",
            "response_time": round(response_time, 3)
        }
    except Exception as e:
        return {"error": str(e)}

def grab_mail_banner(target: str, port: int):
    """Grab mail service banner"""
    try:
        start_time = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((target, port))
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        response_time = time.time() - start_time
        sock.close()
        return {
            "banner": banner,
            "service": "MAIL",
            "response_time": round(response_time, 3)
        }
    except Exception as e:
        return {"error": str(e)}

def grab_ssl_info(target: str, port: int):
    """Grab SSL/TLS certificate information"""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((target, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                return {
                    "certificate": {
                        "subject": dict(x[0] for x in cert['subject']),
                        "issuer": dict(x[0] for x in cert['issuer']),
                        "version": cert['version'],
                        "serial_number": cert['serialNumber'],
                        "not_before": cert['notBefore'],
                        "not_after": cert['notAfter']
                    },
                    "cipher_suite": {
                        "name": cipher[0],
                        "version": cipher[1],
                        "bits": cipher[2]
                    },
                    "protocol_version": ssock.version()
                }
    except Exception as e:
        return {"error": str(e)}

def analyze_security_headers(headers):
    """Analyze security headers"""
    security_headers = {
        "X-Frame-Options": headers.get("X-Frame-Options"),
        "X-Content-Type-Options": headers.get("X-Content-Type-Options"),
        "Strict-Transport-Security": headers.get("Strict-Transport-Security"),
        "Content-Security-Policy": headers.get("Content-Security-Policy"),
        "X-XSS-Protection": headers.get("X-XSS-Protection"),
        "Referrer-Policy": headers.get("Referrer-Policy"),
        "Permissions-Policy": headers.get("Permissions-Policy")
    }
    
    present_headers = [k for k, v in security_headers.items() if v]
    missing_headers = [k for k, v in security_headers.items() if not v]
    
    score = len(present_headers) / len(security_headers) if security_headers else 0
    
    return {
        "present": {k: v for k, v in security_headers.items() if v},
        "missing": missing_headers,
        "score": round(score, 2),
        "grade": "A" if score >= 0.8 else "B" if score >= 0.6 else "C" if score >= 0.4 else "D" if score >= 0.2 else "F"
    }

def assess_service_risk(service_info: dict):
    """Assess risk level based on service type and configuration"""
    
    risk_factors = {
        "database": 8,      # High risk - direct data access
        "remote_access": 7, # High risk - direct system access
        "file_transfer": 5, # Medium risk - file access
        "mail_service": 4,  # Medium risk - communication
        "web_service": 3,   # Lower risk - public facing
        "unknown": 6        # Unknown risk - assume medium-high
    }
    
    base_risk = risk_factors.get(service_info.get("type", "unknown"), 6)
    
    # Adjust risk based on security headers (for web services)
    if service_info.get("type") == "web_service":
        security_score = service_info.get("security_headers", {}).get("score", 0)
        base_risk -= int(security_score * 2)  # Reduce risk for good security headers
    
    risk_score = max(1, min(10, base_risk))  # Clamp between 1-10
    
    # Convert score to risk level
    if risk_score >= 8:
        risk_level = "CRITICAL"
    elif risk_score >= 6:
        risk_level = "HIGH"
    elif risk_score >= 4:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return {
        "score": risk_score,
        "level": risk_level
    }

def checkServices(port: int, target: str):
    """Enhanced service detection with banner grabbing and risk assessment"""
    
    # Web services that can be banner grabbed
    web_services = {
        80: "HTTP",
        443: "HTTPS", 
        8080: "HTTP-ALT",
        8443: "HTTPS-ALT",
        8000: "HTTP-ALT",
        8888: "HTTP-ALT",
        5000: "HTTP-ALT"
    }
    
    # Database services
    db_services = {
        3306: "MySQL",
        5432: "PostgreSQL", 
        1433: "MSSQL",
        1521: "Oracle",
        27017: "MongoDB",
        6379: "Redis"
    }
    
    # File transfer services
    ftp_services = {
        21: "FTP",
        22: "SSH/SFTP",
        990: "FTPS"
    }
    
    # Mail services
    mail_services = {
        25: "SMTP",
        110: "POP3",
        143: "IMAP",
        587: "SMTP-SUBMISSION",
        993: "IMAPS",
        995: "POP3S"
    }
    
    # Remote access services
    remote_services = {
        23: "Telnet",
        3389: "RDP",
        5900: "VNC",
        5901: "VNC-1",
        5902: "VNC-2"
    }
    
    # Combine all service mappings
    all_services = {**web_services, **db_services, **ftp_services, **mail_services, **remote_services}
    
    service_name = all_services.get(port, "unknown")
    
    # Handle web services with banner grabbing
    if service_name in ["HTTP", "HTTPS", "HTTP-ALT", "HTTPS-ALT"]:
        protocol = "https" if "HTTPS" in service_name else "http"
        url = f"{protocol}://{target}:{port}"
        banner_info = grab_http_banner(url)
        security_headers = analyze_security_headers(banner_info.get("headers", {}))
        
        service_info = {
            "name": service_name,
            "type": "web_service",
            "banner": banner_info,
            "security_headers": security_headers
        }
        
        # Add SSL info for HTTPS
        if "HTTPS" in service_name:
            ssl_info = grab_ssl_info(target, port)
            service_info["ssl_info"] = ssl_info
        
        risk_assessment = assess_service_risk(service_info)
        service_info["risk_assessment"] = risk_assessment
        
        return service_info
    
    # Handle database services
    elif service_name in ["MySQL", "PostgreSQL", "MSSQL", "Oracle", "MongoDB", "Redis"]:
        service_info = {
            "name": service_name,
            "type": "database",
            "banner": grab_mail_banner(target, port),  # Use generic banner grabber
            "risk_assessment": {"score": 8, "level": "HIGH"},
            "recommendation": f"Database service {service_name} exposed on port {port}. Consider restricting access to trusted IPs only."
        }
        return service_info
    
    # Handle file transfer services
    elif service_name in ["FTP", "SSH/SFTP", "FTPS"]:
        banner_info = grab_ftp_banner(target, port)
        risk_level = "MEDIUM" if service_name == "SSH/SFTP" else "HIGH"
        risk_score = 5 if service_name == "SSH/SFTP" else 7
        
        service_info = {
            "name": service_name,
            "type": "file_transfer",
            "banner": banner_info,
            "risk_assessment": {"score": risk_score, "level": risk_level},
            "recommendation": f"File transfer service {service_name} exposed on port {port}. Ensure strong authentication is configured."
        }
        return service_info
    
    # Handle mail services
    elif service_name in ["SMTP", "POP3", "IMAP", "SMTP-SUBMISSION", "IMAPS", "POP3S"]:
        banner_info = grab_mail_banner(target, port)
        service_info = {
            "name": service_name,
            "type": "mail_service",
            "banner": banner_info,
            "risk_assessment": {"score": 4, "level": "MEDIUM"},
            "recommendation": f"Mail service {service_name} exposed on port {port}. Configure proper authentication and encryption."
        }
        return service_info
    
    # Handle remote access services
    elif service_name in ["Telnet", "RDP", "VNC", "VNC-1", "VNC-2"]:
        banner_info = grab_mail_banner(target, port)  # Use generic banner grabber
        service_info = {
            "name": service_name,
            "type": "remote_access",
            "banner": banner_info,
            "risk_assessment": {"score": 7, "level": "HIGH"},
            "recommendation": f"Remote access service {service_name} exposed on port {port}. This is a high-risk exposure. Consider VPN access instead."
        }
        return service_info
    
    # Unknown service
    banner_info = grab_mail_banner(target, port)  # Try generic banner grabber
    service_info = {
        "name": service_name,
        "type": "unknown",
        "banner": banner_info,
        "risk_assessment": {"score": 6, "level": "MEDIUM"},
        "recommendation": f"Unknown service on port {port}. Investigate and secure if not needed."
    }
    return service_info

def scan_ports(target, isGUI):
    if is_ip_address(target):
        print("Please Enter a valid Domain (example.com).")
        return
    
    print(f"🔍 Enhanced port scanning on: {target}")
    
    # Clean target
    secured = None
    if target.__contains__('https://'):
        secured = True
        target = target.replace('https://', '')
    elif target.__contains__('http://'):
        secured = False
        target = target.replace('http://', '')
    
    target_url = []
    open_ports = []
    services = {}
    scan_logs = []
    risk_summary = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }
    
    if check_protocol(target):
        scan_logs.append(f"✅ Protocol check passed for {target}")
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((target, port))
                if result == 0:
                    print(f"🔓 Port {port} is open - analyzing service...")
                    open_ports.append(port)
                    
                    # Enhanced service detection
                    service_info = checkServices(port, target)
                    services[port] = service_info
                    
                    # Update risk summary
                    risk_level = service_info.get("risk_assessment", {}).get("level", "UNKNOWN")
                    if risk_level == "CRITICAL":
                        risk_summary["critical"] += 1
                    elif risk_level == "HIGH":
                        risk_summary["high"] += 1
                    elif risk_level == "MEDIUM":
                        risk_summary["medium"] += 1
                    else:
                        risk_summary["low"] += 1
                    
                    scan_logs.append(f"🔍 Port {port}: {service_info['name']} ({service_info['type']}) - Risk: {risk_level}")
                    
                sock.close()
            except Exception as e:
                scan_logs.append(f"❌ Error scanning port {port}: {str(e)}")
    
    if len(open_ports) >= 1:
        # Create target URLs for web services
        for port in open_ports:
            service_info = services.get(port, {})
            if service_info.get("type") == "web_service":
                protocol = "https" if "HTTPS" in service_info.get("name", "") else "http"
                target_url.append(f"{protocol}://{target}:{port}")
        
        # If no web services found, create default URLs
        if not target_url:
            if secured:
                target_url.append(f"https://{target}")
            else:
                target_url.append(f"http://{target}")
        
        if isGUI:
            return {
                "open_ports": open_ports,
                "services": services,
                "target_urls": target_url,
                "scan_logs": scan_logs,
                "risk_summary": risk_summary,
                "scan_timestamp": datetime.now().isoformat()
            }
        else:
            # CLI output
            print(f"\n📊 Scan Results for {target}:")
            print(f"Open Ports: {len(open_ports)}")
            print(f"Risk Summary: {risk_summary}")
            
            for port in open_ports:
                service_info = services[port]
                print(f"\n🔍 Port {port}: {service_info['name']}")
                print(f"   Type: {service_info['type']}")
                print(f"   Risk: {service_info['risk_assessment']['level']} ({service_info['risk_assessment']['score']}/10)")
                if service_info.get('recommendation'):
                    print(f"   Recommendation: {service_info['recommendation']}")
            
            if secured:
                target_url.append(f"https://{target}")
                run_gobuster_scan(target_url)
            else:
                target_url.append(f"http://{target}")
                run_gobuster_scan(target_url)
    else:
        print("❌ No ports open, please try another domain.")
        scan_logs.append("❌ No open ports found")
        if isGUI:
            return {
                "open_ports": [],
                "services": {},
                "target_urls": [],
                "scan_logs": scan_logs,
                "risk_summary": risk_summary,
                "scan_timestamp": datetime.now().isoformat()
            }