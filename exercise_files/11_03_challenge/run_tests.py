import sys
import subprocess


def run_tests():
    print("🔍 Running tests with pytest...")
    result = subprocess.run(["pytest", "tests", "--tb=short", "-v"])
    if result.returncode != 0:
        print("❌ Tests failed.")
        sys.exit(result.returncode)
    print("✅ All tests passed.")


def run_coverage():
    print("\n📊 Generating coverage report...")
    subprocess.run(
        ["coverage", "run", "--source=canvas,scribes,utils", "-m", "pytest", "tests"]
    )
    subprocess.run(["coverage", "report", "-m"])
    subprocess.run(["coverage", "html"])
    print("📂 HTML report generated in htmlcov/index.html")


if __name__ == "__main__":
    if "--coverage" in sys.argv:
        run_coverage()
    else:
        run_tests()
