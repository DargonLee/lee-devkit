
Pod::Spec.new do |s|
  s.name             = 'NBTemplateModule'
  s.version          = '0.1.0'
  s.summary          = 'A short description of NBTemplateModule.'
  s.description      = <<-DESC
TODO: Add long description of the pod here.
                       DESC
  s.homepage         = 'https://git.ninebot.com/'
  s.license          = { :type => 'MIT', :file => 'LICENSE' }
  s.author           = { 'ninebot' => 'www.ninebot.com' }
  s.source           = { :git => 'https://git.ninebot.com/iOS/NBTemplateModule.git', :tag => s.version.to_s }

  s.ios.deployment_target = '13.0'
  s.source_files = 'NBTemplateModule/Sources/**/*'
  

  type = ENV['type'] == 'overseas' ? 'Overseas' : 'China'
  s.resource_bundles = {
    'NBTemplateModule' => ["NBTemplateModule/Resources/#{type}/**/*.*"]
  }

  
  # s.frameworks = 'UIKit', 'MapKit'
  # s.dependency 'AFNetworking', '~> 2.3'
end
